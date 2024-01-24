from robocorp import browser
import robocorp.workitems

class Browser:
    def __init__(self, path: str) -> None:
        
        # inputs  = robocorp.workitems.Inputs()
        # item    = inputs.reserve()  
        # payload = item.payload

        self.site:str = 'https://www.google.com/'
        
        try:
            # # browser.goto(self.site)
            # # with open("teste.txt","w") as file:
            # #     file.write("Hello Robocloud!")
            # inputs = robocorp.workitems.Inputs()

            # # Reserve um workitem da fila
            # item = inputs.reserve()

            # # Acesse o payload do workitem
            # payload = item.payload

            # Crie um novo arquivo TxR
            with open("teste.txt", "w") as f:
                f.write("hello robocorp")

            # Libere o workitem da fila
            # inputs.release(item)
        except:
            print("Error on open browser")