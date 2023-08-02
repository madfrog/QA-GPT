# coding=utf-8

from llama_index import ListIndex, ServiceContext, StorageContext, load_graph_from_storage, SimpleKeywordTableIndex
from llama_index.indices.composability import ComposableGraph
from llama_index.indices.query.query_transform.base import DecomposeQueryTransform
from llama_index.query_engine.transform_query_engine import TransformQueryEngine
import index_builder
from tools.file_helper import FileHelper


class QueryEngineBuilder(object):
    def __init__(self, service_context, llm_predictor, index_set, file_names, logger):
        self._service_context = service_context
        self._llm_predictor = llm_predictor
        self.__logger = logger

        # set summary text for each doc
        # file_names = FileHelper.get_all_file_names(f'{index_builder.FILE_FOLDER}/{index_builder.NEWEST_FOLDER}')
        index_summaries = {}
        for name in file_names:
            company_name, year, company_year = FileHelper.get_company_name_and_year(name)
            index_summaries[company_year] = (
                f"This content contains 10-k filing about {company_name} in {year}."
                f"Use this index if you need to lookup specific facts about {company_name}."
                "Do not use this index if you want to analyze multiple cities."
            )
        self._index_set = index_set
        self._index_summaries = index_summaries
        logger.debug(f'index set len: {len(self._index_set)}, index summaries len: {len(self._index_summaries)}')

    def build_query_engine(self):
        # set the graph
        graph = ComposableGraph.from_indices(
            SimpleKeywordTableIndex,
            [index for _, index in self._index_set.items()],
            [summary for _, summary in self._index_summaries.items()],
            max_keywords_per_chunk = 50
        )
        # get root index
        root_index = graph.get_index(graph.index_struct.index_id)
        # set id of root index
        # what is this index for?
        root_index.set_index_id("compare_contrast")
        root_summary = (
             "This index contains 10-k filing about multiple companies."
             "Use this index if you want to compare multiple companies."
         )

        # define decompose_transsform
        decompose_transsform = DecomposeQueryTransform(self._llm_predictor, verbose=True)
        
        # define custom query engines
        custom_query_engines = {}
        for index in self._index_set.values():
            query_engine = index.as_query_engine(service_context=self._service_context)
            transform_query_engine = TransformQueryEngine(
                query_engine,
                query_transform=decompose_transsform,
                transform_metadata={'index_summary': index.index_struct.summary},
            )
            custom_query_engines[index.index_id] = transform_query_engine
        custom_query_engines[graph.root_id] = graph.root_index.as_query_engine(
            retriever='simple',
            response='tree_summaries',
            service_context=self._service_context,
        )

        return graph.as_query_engine(custom_query_engines=custom_query_engines)




