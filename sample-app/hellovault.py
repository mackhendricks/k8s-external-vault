from flask import Flask, render_template
import os
app = Flask(__name__)

@app.route("/")
def hellovault():
    # Dictionary object just to hold App Specific Environment Variables
    appEnvList={}
    if os.environ.items():
        for k, v in os.environ.items():
            if k.startswith("APP"):
                appEnvList[k]=v
    #return "Print Dictionary {}:".format(appEnvList)
    return render_template('hellovault.html', envlist=appEnvList)

if __name__ == "__main__":
    app.run()
