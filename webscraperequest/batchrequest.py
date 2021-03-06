import doctest
import functools
import time  # noqa

from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple, Type
from unittest import mock  # noqa

from django.db import models

try:
    from .scraperequest import *
except ModuleNotFoundError:
    # For doctest, which is not run in package context
    from scraperequest import *  # type: ignore # noqa

logger = logging.getLogger(__name__)


class BaseBatchWebRequest:
    """
    Manages a parallel batch of web requests. Intermediate and final results are
    saved into a given Django model instance.

    There are two abstract properties to override: requester and field_name.

    There are two public methods: start and get_batch_status.
    """

    max_workers = 8  # Number of threads to use

    def __init__(self, model_instance: models.Model) -> None:
        self.model_instance = model_instance

    requester: Type[AbstractScrapeRequest]

    @property
    @staticmethod
    @abstractmethod
    def field_name() -> str:
        """The field name of model_instance that should contain request results."""

    def start(self, largs: List[list], keys: List[int] = []) -> None:
        """Start all requests, each in a thread, with the given list of args"""
        self._init_instance_field(largs, keys)

        pool = ThreadPoolExecutor(self.max_workers)
        for i, args in enumerate(largs):
            logger.debug('{} submitted to thread pool'.format(self.requester.__class__))
            pool.submit(self._request, args).add_done_callback(
                functools.partial(self._insert, index=i))
        pool.shutdown(wait=False)

    def get_batch_status(self) -> 'BatchStatus':  # forward ref for typing
        completed, running, errorred = [], [], []
        current_results = getattr(self.model_instance, str(self.field_name))
        for i, result in enumerate(current_results):
            key = tuple([i,
                         # result['cache_key'],
                         # result['success']
                         ] + result['request_key'])
            if result['in_cache']:
                key += ('in cache',)
            if result['success'] is True:
                duration = round(result['end_time'] - result['start_time'], 1)
                key += (f'{duration}s',)
                completed.append(key)
            elif result['success'] is False:
                errorred.append(key + (result['error'],))
            elif result['success'] is None:
                running.append(key)
            else:
                assert False

        return BatchStatus(completed, errorred, running)

    def _init_instance_field(self, largs: List[list], keys: List[int]) -> None:
        setattr(self.model_instance, str(self.field_name), [
            {'success': None,
             'request_key': [args[k] for k in keys],
             'in_cache': self.requester(*args).in_cache(),  # type: ignore
             'cache_key': self.requester(*args).cache_key,  # type: ignore
             'start_time': time.time()}
            for i, args in enumerate(largs)
        ])
        self.model_instance.save()
        logger.debug('{} initial values saved'.format(self.requester.__class__))

    def _request(self, args: list) -> Dict[str, Any]:
        try:
            return self.requester(*args).run()  # type: ignore
        except (Exception) as e:
            logger.exception(e)
            return {
                'success': False,
                'error': getattr(e, 'message', str(e)),
            }

    def _insert(self, future, index=None) -> None:
        try:
            result = future.result()
            result['success'] = result.get('success', True)
            logger.debug('{} result inserted into database'.format(self.requester.__class__))
        except Exception as e:
            logger.error('Error inserting into index {}: {}'
                         .format(index, str(e)))
            result['success'] = result.get('success', False)
            result['error'] = getattr(e, 'message', str(e))
        finally:
            result['end_time'] = int(time.time())
            self.model_instance.__dict__[str(self.field_name)][index].update(result)
            self.model_instance.save()


class BatchStatus:

    def __init__(
        self,
        completed: Sequence[Tuple[Any, ...]],
        errored: Sequence[Tuple[Any, ...]],
        running: Sequence[Tuple[Any, ...]],
    ) -> None:
        self.completed = completed
        self.errored = errored
        self.running = running

    def __str__(self) -> str:
        return 'BatchStatus({}, {}, {})'.format(
            self.completed, self.errored, self.running)

    @property
    def statuses(self):
        return self.completed + self.errored + self.running

    @property
    def percent_success(self):
        return 100 * len(self.completed) // len(self.statuses)

    @property
    def percent_error(self):
        return 100 * len(self.errored) // len(self.statuses)

    @property
    def is_done(self):
        return not self.running

    @property
    def is_successful(self):
        return len(self.completed) == len(self.statuses)


class CrisporGuideBatchWebRequest(BaseBatchWebRequest):
    """
    >>> batch = CrisporGuideBatchWebRequest(mock.Mock())
    >>> largs = [['chr1:11,130,540-11,130,751'], ['chr1:1-1']]
    >>> batch.start(largs)
    >>> print(batch.get_batch_status())
    BatchStatus([], [], [(0, 'in cache'), (1, 'in cache')])
    >>> time.sleep(1)
    >>> print(batch.get_batch_status()) # doctest: +ELLIPSIS
    BatchStatus([(0, 'in cache', ...)], [(1, 'in cache', 'Crispor on chr1:1-1: Bad sequence size: 8')], [])
    """
    requester = CrisporGuideRequest
    field_name = 'guide_data'
    # More than 8 threads appears to cause a 'no output' Crispor error
    # TODO (gdingle): create global worker pool? somehow?
    max_workers = 4


class CrisporPrimerBatchWebRequest(BaseBatchWebRequest):
    """
    >>> batch = CrisporPrimerBatchWebRequest(mock.Mock())
    >>> largs = [['9cJNEsbfWiSKa8wlaJMZ', 's185+']]
    >>> batch.start(largs, [0, 1])
    >>> print(batch.get_batch_status())
    BatchStatus([], [], [(0, '', '9cJNEsbfWiSKa8wlaJMZ', 's185+')])
    >>> time.sleep(1)
    >>> print(batch.get_batch_status()) # doctest: +ELLIPSIS
    BatchStatus([], [], [(0, '', '9cJNEsbfWiSKa8wlaJMZ', 's185+')])
    """
    requester = CrisporPrimerRequest
    field_name = 'primer_data'
    max_workers = 4


class CrispressoBatchWebRequest(BaseBatchWebRequest):
    """
    >>> batch = CrispressoBatchWebRequest(mock.Mock())
    >>> amplicon = 'cgaggagatacaggcggagggcgaggagatacaggcggagggcgaggagatacaggcggagagcgGCGCTAGGACCCGCCGGCCACCCCGCCGGCTCCCGGGAGGTTGATAAAGCGGCGGCGGCGTTTGACGTCAGTGGGGAGTTAATTTTAAATCGGTACAAGATGGCGGAGGGGGACGAGGCAGCGCGAGGGCAGCAACCGCACCAGGGGCTGTGGCGCCGGCGACGGACCAGCGACCCAAGCGCCGCGGTTAACCACGTCTCGTCCAC'
    >>> sgRNA = 'AATCGGTACAAGATGGCGGA'
    >>> fastq_r1 = '../crispresso/fastqs/A1-ATL2-N-sorted-180212_S1_L001_R1_001.fastq.gz'
    >>> fastq_r2 = '../crispresso/fastqs/A1-ATL2-N-sorted-180212_S1_L001_R2_001.fastq.gz'
    >>> largs = [[amplicon, sgRNA, fastq_r1, fastq_r2]]
    >>> batch.start(largs)
    >>> print(batch.get_batch_status())
    BatchStatus([], [], [(0, 'in cache')])
    >>> time.sleep(4)
    >>> print(batch.get_batch_status()) # doctest: +ELLIPSIS
    BatchStatus([(0, ...)], [], [])
    """
    requester = CrispressoRequest
    field_name = 'results_data'
    max_workers = 4

    @staticmethod
    def _get_primer_product(row, analysis) -> str:
        """
        This is complicated because of HDR, non-HDR, and custom sheet name mangling.
        """
        if analysis.experiment.is_hdr or analysis.is_custom:
            if '_primer_product_wt' in row and row['_primer_product_wt']:
                return row['_primer_product_wt']
            elif 'primer_product_wt' in row and row['primer_product_wt']:
                return row['primer_product_wt']

        return row['primer_product']

    @staticmethod
    def _get_primer_product_after_hdr(row, analysis) -> str:
        if CrispressoBatchWebRequest._get_primer_product(row, analysis) == row['primer_product']:
            return ''
        else:
            return row['primer_product']

    @staticmethod
    def start_analysis(
            analysis: models.Model,
            records: Iterable[Mapping[str, str]]) -> None:

        batch = CrispressoBatchWebRequest(analysis)
        largs = [[
            CrispressoBatchWebRequest._get_primer_product(row, analysis),
            row['guide_seq'],
            row['fastq_fwd'],
            row['fastq_rev'],
            row['_primer_adapt_name'] if '_primer_adapt_name' in row else row['primer_adapt_name'],
            # "amplicon" in crispresso
            # TODO (gdingle): rename primer_product in CC ?
            CrispressoBatchWebRequest._get_primer_product_after_hdr(row, analysis),
            row['target_input'] if 'target_input' in row else 'asdf',
        ] for row in records]
        return batch.start(largs, [-1, 1])


if __name__ == '__main__':
    # TODO (gdingle): re-run tests on new crispor server, save in cache
    doctest.testmod()
