# -*- coding: utf-8 -*-

# chinese computing project
# members: Mo Feiyu, Sun Rui, Wang Zizhe, copyright


# pickle file of conversations must exist, config.file_dict and config.index_dict must be right


from retrieval_documents import BuildIndex
import config

build_index = BuildIndex(config)
build_index.load_pickle()
build_index.build_index()
