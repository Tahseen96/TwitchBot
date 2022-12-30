import eel
from bot import main
  
# Exposing the random_python function to javascript
@eel.expose    
def run_main():
    main(eel)
  
# Start the index.html file
if __name__ == '__main__':
    eel.init("web")  
    eel.start("index.html", size=(374, 630), port=0, mode='chrome')