# Gerador de metricas de um computador de bordo

#### Colaboradores: Ariel Adonai Souza, Gabriel Castellani de Oliveira e Gabriel Luís Fernando de Souza.

## Trabalho de sistemas distribuidos

Nosso trabalho utiliza um raspberry que se comunica com a porta OBD2 do carro e recupera metricas do carro dentre elas, a temperatura da água, rotações por minuto, velocidade e quaisquer outras que a central do carro disponibiliza depois disso, interpreta essas informações e envia para endpoint API Gateway que dispara um `Lambda` que salva essas informações em um `DynamoDB`.

### Payload enviado para o DynamoDB:
```json
    {
	"date": "2019/05/28T21:05:15Z",
	"car": "GOL_G4_2009_MFBXXXX",
	"speed": 0.0,
	"rpm": 855.75,
	"intake_temp": 31.0,
	"oil_temp": null,
	"coolant_temp": 87.0,
	"latitude": null,
	"longetude": null,
	"id": "GOL_G4_2009_MFBXXXX_2019/05/28T21:05:15Z"
}
```

Após isso, consumimos os dados em um grafana utilizando uma API REST que lê os dados do `DynamoDB` filtrando pelos parâmetros informados pelo grafana e retorna no padrão de payload do plugin [Simple JSON](https://grafana.com/plugins/grafana-simple-json-datasource) do grafana

### Payload de request do Grafana:
```json
{
  "timezone": "browser",
  "panelId": 8,
  "dashboardId": 2,
  "range": {
    "from": "2019-05-27T23:16:02.391Z",
    "to": "2019-05-27T23:27:52.506Z",
    "raw": {
      "from": "2019-05-27T23:16:02.391Z",
      "to": "2019-05-27T23:27:52.506Z"
    }
  },
  "rangeRaw": {
    "from": "2019-05-27T23:16:02.391Z",
    "to": "2019-05-27T23:27:52.506Z"
  },
  "interval": "1s",
  "intervalMs": 1000,
  "targets": [
    {
      "target": "coolant_temp",
      "refId": "A",
      "type": "timeserie"
    }
  ],
  "maxDataPoints": 927,
  "scopedVars": {
    "__interval": {
      "text": "1s",
      "value": "1s"
    },
    "__interval_ms": {
      "text": 1000,
      "value": 1000
    }
  },
  "adhocFilters": []
}

```

### Payload de response para o Grafana:
```json
[
    {
      "datapoints": [
        [
          55,
          1558998977000
        ],
        [
          56,
          1558998986000
        ],
        [
          56,
          1558998987000
        ],
        [
          57,
          1558998991000
        ],
        [
          57,
          1558998995000
        ],
        [
          57,
          1558999007000
        ],
        [
          58,
          1558999010000
        ],
        [
          58,
          1558999013000
        ],
        [
          60,
          1558999026000
        ],
        ...
      ],
      "target": "coolant_temp"
    }
  ]
```

E então o grafana monta graficos para as métricas informadas:

![imagem-grafana](https://github.com/arielrenostro/car-messages/blob/master/resources/f45d3ea3-0398-4ab0-993a-5e21ddaada3f.jpeg)

### Dados Para acesso ao grafana:

Endereço: [http://arielrenostro.ddns.net:3000/](http://arielrenostro.ddns.net:3000/d/xEzPtRGWk/car?orgId=1&from=1559076498917&to=1559077738477)  
Usuário: viewer  
Senha: viewer 

# Stack de desenvolvimento

* [Leitor OBD2 Bluetooth EML327](https://www.elmelectronics.com/wp-content/uploads/2016/07/ELM327DS.pdf)
* [Raspberry Pi 3 Model B](https://www.raspberrypi.org/)
* [AWS EC2](https://aws.amazon.com/pt/ec2/)
* [AWS Lambda](https://aws.amazon.com/pt/lambda/)
* [AWS DynamoDB](https://aws.amazon.com/pt/dynamodb/)
* [AWS API Gateway](https://aws.amazon.com/pt/api-gateway/)
* [Grafana](https://grafana.com/)
* [Docker](https://hub.docker.com/)
* [Python](https://www.python.org/)
* [Requests](https://2.python-requests.org/en/master/)
* [Flask](http://flask.pocoo.org/)