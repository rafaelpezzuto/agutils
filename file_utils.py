import sys
import os

sys.path.append('../aglattes/')
from models.lattes import Lattes, Relacao


class FileUtils(object):

    CABECALHO_GDF_VERTICE = 'nodedef>name VARCHAR,label VARCHAR,nome_ultima_titulacao VARCHAR,ano_ultima_titulacao INTEGER,eh_livre_docente BOOLEAN,ano_primeira_livre_docencia INTEGER,tem_pos_doc BOOLEAN,ano_primeiro_pos_doc INTEGER,primeira_grande_area VARCHAR,primeira_area VARCHAR,primeira_sub_area VARCHAR,primeira_especialidade VARCHAR,eh_ascendente BOOLEAN,eh_descendente BOOLEAN,eh_semente BOOLEAN,profi_instituicao VARCHAR,profi_orgao VARCHAR,profi_pais VARCHAR,profi_uf VARCHAR,profi_cidade VARCHAR,profi_bairro VARCHAR,profi_logradouro VARCHAR,profi_cep VARCHAR,pais_de_nascimento VARCHAR,uf_nascimento VARCHAR,cidade_nascimento VARCHAR,nacionalidade VARCHAR,pais_de_nacionalidade VARCHAR,sigla_pais_nacionalidade VARCHAR,data_ultima_atualizacao_curriculo VARCHAR'

    CABECALHO_GDF_ARESTA = 'edgedef>origem_id_lattes,destino_id_lattes,origem_nome VARCHAR,destino_nome VARCHAR,titulacao VARCHAR,codigo_nivel VARCHAR,tipo_orientacao VARCHAR,ano_inicio INTEGER,ano_conclusao INTEGER,curso VARCHAR,instituicao VARCHAR,tese VARCHAR,extra VARCHAR,grande_area VARCHAR,area VARCHAR,sub_area VARCHAR,especialidade VARCHAR,directed BOOLEAN'


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


    @staticmethod
    def vertice_to_gdf(vertice: Lattes):
        gdf_vertice = []
        gdf_vertice.append(vertice.id_lattes)
        gdf_vertice.append(vertice.nome.title())
        gdf_vertice.append(vertice.nome_ultima_titulacao.title())
        gdf_vertice.append(vertice.ano_ultima_titulacao)
        gdf_vertice.append(vertice.eh_livre_docente)
        gdf_vertice.append(vertice.ano_primeira_livre_docencia)
        gdf_vertice.append(vertice.tem_pos_doc)
        gdf_vertice.append(vertice.ano_primeiro_pos_doc)
        gdf_vertice.append(vertice.primeira_grande_area.title())
        gdf_vertice.append(vertice.primeira_area.title())
        gdf_vertice.append(vertice.primeira_sub_area.title())
        gdf_vertice.append(vertice.primeira_especialidade.title())
        gdf_vertice.append(vertice.eh_ascendente)
        gdf_vertice.append(vertice.eh_descendente)
        gdf_vertice.append(vertice.eh_semente)
        gdf_vertice.append(vertice.profi_instituicao.title())
        gdf_vertice.append(vertice.profi_orgao.title())
        gdf_vertice.append(vertice.profi_pais.title())
        gdf_vertice.append(vertice.profi_uf.upper())
        gdf_vertice.append(vertice.profi_cidade.title())
        gdf_vertice.append(vertice.profi_bairro.title())
        gdf_vertice.append(vertice.profi_logradouro.title())
        gdf_vertice.append(vertice.profi_cep)
        gdf_vertice.append(vertice.pais_de_nascimento.title())
        gdf_vertice.append(vertice.uf_nascimento.upper())
        gdf_vertice.append(vertice.cidade_nascimento.title())
        gdf_vertice.append(vertice.nacionalidade.upper())
        gdf_vertice.append(vertice.pais_de_nacionalidade.title())
        gdf_vertice.append(vertice.sigla_pais_nacionalidade.upper())
        gdf_vertice.append(vertice.data_ultima_atualizacao_curriculo)
        return ','.join(gdf_vertice)

    @staticmethod
    def aresta_to_gdf(aresta: Relacao):
        gdf_aresta = []
        gdf_aresta.append(aresta.origem_id_lattes)
        gdf_aresta.append(aresta.destino_id_lattes)
        gdf_aresta.append(aresta.origem_nome.title())
        gdf_aresta.append(aresta.destino_nome.title())
        gdf_aresta.append(aresta.titulacao.title())
        gdf_aresta.append(aresta.codigo_nivel.title())
        gdf_aresta.append(aresta.tipo_orientacao.title())
        gdf_aresta.append(aresta.ano_inicio)
        gdf_aresta.append(aresta.ano_conclusao)
        gdf_aresta.append(aresta.curso.title())
        gdf_aresta.append(aresta.instituicao.title())
        gdf_aresta.append(aresta.tese.title())
        gdf_aresta.append(aresta.extra.title())
        gdf_aresta.append(aresta.grande_area.title())
        gdf_aresta.append(aresta.area.title())
        gdf_aresta.append(aresta.sub_area.title())
        gdf_aresta.append(aresta.especialidade.title())
        gdf_aresta.append('True')
        return ','.join(gdf_aresta)
    