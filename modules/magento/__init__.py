from . import mag_get_produto, mag_json_filters, mag_put_produto

#exportar funções mais usadas diretamente:
get_produto = mag_get_produto.buscar_dados_produto
put_produto = mag_put_produto.enviar_dados_produto

filter_descricao = mag_json_filters.filter_descricao
filter_nome = mag_json_filters.filter_nome
filter_createdAt = mag_json_filters.filter_createdAt
filter_updatedAt = mag_json_filters.filter_updatedAt
filter_sku = mag_json_filters.filter_sku
filter_ean = mag_json_filters.filter_ean
filter_marca = mag_json_filters.filter_marca
filter_categoriaGoogle = mag_json_filters.filter_categoriaGoogle
filter_conteudoEmbalagem = mag_json_filters.filter_conteudoEmbalagem
filter_peso = mag_json_filters.filter_peso
filter_largura = mag_json_filters.filter_largura
filter_altura = mag_json_filters.filter_altura
filter_comprimento = mag_json_filters.filter_comprimento
filter_metaTitle = mag_json_filters.filter_metaTitle
filter_metaDescription = mag_json_filters.filter_metaDescription
filter_url = mag_json_filters.filter_url