import zmq

# Conectar ao Meta Trader
def remote_send(socket, data):
    try:
        socket.send_string(data)
        msg = socket.recv_string()
        return (msg)
    except zmq.Again as e:
        print ("Aguardando o PUSH do MT5 ...")       

# Obter o contexto do zmq
context = zmq.Context()
# Criar um Socket para as requisições
reqSocket = context.socket(zmq.REQ)
reqSocket.connect("tcp://localhost:5555")

