from sauce_demo import E_Commerce
from fakturama import FakturamaActivities


# Coleta dados do comprador
E_Commerce.fake_data()
# Acessa a loja virtual, coleta os dados de produto e realiza compra
E_Commerce.sauce_demo()
# Cadastra o contato do comprador no Fakturama
FakturamaActivities.cadastra_contato()
# Cadastra a base de produtos da loja virtual no Fakturama
FakturamaActivities.cadastra_produtos()
# Replica ordem de compra no Fakturama e salva em PDF para auditoria
FakturamaActivities.preenche_ordem()
