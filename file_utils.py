import os


class FileUtils(object):

    @staticmethod
    def get_models_from_str_list(str_splitted_objects: list, model=object):
        """
        Receive a list of objects in str representation and a model representation.
        Returns a list of objects in the model representation.
        """
        parsed_objects = []
        header = [h.split(' ')[0] for h in str_splitted_objects.pop(0)]

        for o_attr in str_splitted_objects:
            dargs = {}
            for i, na in enumerate(o_attr):
                dargs[header[i]] = o_attr[i]
            obj = model(**dargs)
            parsed_objects.append(obj)

        return parsed_objects


    @staticmethod
    def get_models_from_path_csv(path_csv: str, sep=',', model=object):
        """
        Receive the path of a file with the objects' str representation and a model representation.
        Returns a list of the objects parsed to the model representation.
        """
        parsed_objects = []
        file_data = open(path_csv)
        tmp_objects = [r.strip() for r in file_data]
        header = tmp_objects.pop(0).strip().split(sep)

        for r in tmp_objects:
            attributes = r.strip().split(sep)
            dargs = {}
            for i, na in enumerate(attributes):
                dargs[header[i]] = attributes[i]
            obj = model(**dargs)
            parsed_objects.append(obj)
        file_data.close()

        return parsed_objects


    @staticmethod
    def get_str_vertices_and_edges_from_path_gdf_graph(path_gdf_graph: str, sep=',', nattr_vertices=30, nattr_edges=18):
        """
        Receive the path of a gdf file and the numbers of vertices and edges attributes.
        Returns the lists of vertices and edges in splitted str format.
        """
        _str_vertices = []
        _str_edges = []

        file_graph = open(path_gdf_graph)

        for line in file_graph:
            els = line.strip().split(',')
            if len(els) == nattr_vertices:
                _str_vertices.append(els)
            elif len(els) == nattr_edges:
                _str_edges.append(els)

        file_graph.close()

        return _str_vertices, _str_edges

    
    @staticmethod
    def save_subgraphs(path_base_dir_subgraph: str, subgraphs: dict):
        """
        Receive the base folder's path and a dict of subgraphs.
        Write in the disk a file for each subgraph for the dict of subgraphs.
        """
        os.makedirs(path_base_dir_subgraph)
        for k in subgraphs:
            k_edges = subgraphs.get(k)

            subgraph_name = k.title().replace(' ', '')
            if subgraph_name == '':
                subgraph_name = 'Desconhecido'

            file_k = open(path_base_dir_subgraph + subgraph_name + '.csv', 'w')
            file_k.write(k_edges[0].get_header() + '\n')
            for e in k_edges:
                file_k.write(e.get_attributes() + '\n')
            file_k.close()
    