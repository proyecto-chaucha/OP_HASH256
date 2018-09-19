# OP_HASH256

Colección de scripts para ejecutar **transacciones puzzle** en la red de [Chaucha](https://ww.chaucha.cl)

## Introducción

La creación de una transacción de criptomonedas es considerada válida cuando la ejecución del [script](https://en.bitcoin.it/wiki/Script) entrega un valor
verdadero (1), y es rechazada por la red al entregar un valor falso (0).

Este script consta de dos elementos, el **ScriptPubKey** que está adjunto a la
entrada (unspent) de la transacción a diseñar, y el **SigScript** que le entrega
las variables necesarias para que la transacción creada sea válida.

En este ejemplo se utilizó la capacidad de las direcciones P2SH para almacenar
parte del código del script, a modo de que sea posible conformar una solución
válida en el futuro si se desean extraer las Chauchas almacenadas en esta
dirección P2SH.

El script diseñado es el siguiente:

```
<solución> OP_HASH256 <SHA256(SHA256(solución))> OP_EQUAL
```

Este script solo es válido cuando se compara una palabra secreta (llamada
*solución*) con respecto al doble hash de la misma, lo que permite diseñar una transacción válida dirigida a ningún destinatario explicito.

## Modo de uso

### Creación de dirección de almacenamiento

```
$>python3 create.py "<solución del puzzle>"
> P2SH address: <dirección de almacenamiento>
```

### Ejecución de contrato en la red

```
$>python3 spend.py "<solución del puzzle>" <dirección de destino>
> Transaction broadcasted, {"txid":"<transaction id>"}
```
