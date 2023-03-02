# SD-TRAB-02
Implementação do load balancer para o trabalho 2 de sistemas distribuídos.

Enunciado:

Desenvolva um Balanceador de Carga que receba conexões e seja capaz de enviar o tráfego para três diferentes servidores (S1, S2 e S3). Dois algoritmos devem ser implementados:
1) Round Robin padrão
2) Encaminhamento baseado no tipo de conexão (TCP ou UDP). Nesse algoritmo, S1 deve receber as conexões TCP, S2 e S3 devem receber as conexões UDP. A distribuição entre S2 e S3 deve usar o algoritmo Round Robin.

Para a execução do Balanceador de carga, deve ser passado um parâmetro numérico para a escolha do algoritmo.

Pode ser feito em duplas.