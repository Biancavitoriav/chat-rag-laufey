# Este script Python no nivel mais alto da aplicacao
# define a instancia da aplicaçao Flask. Por enquanto, ele 
# tem somente uma linha que importa a instancia da aplicacao.
# A aplicacao Flask chama-se 'app' e faz parte do pacote 'app'.
from app import app

 
if __name__ == "__main__":
    app.run(debug=True)
 