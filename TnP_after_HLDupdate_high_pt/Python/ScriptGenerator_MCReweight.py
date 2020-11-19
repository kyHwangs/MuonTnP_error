class ScriptGenerator:
    def __init__(self):
        self.scriptName = ""
        self.reweightCode = ""

        self.inputData = ""
        self.inputMC = ""
        self.outputMC = ""


        # -- internal variable
        self.List_CMD = []

    def Generate(self):
        f_script = open(self.scriptName, "w")

        f_script.write("#!/bin/bash\n\n")

        for CMD in self.List_CMD:
            f_script.write(CMD)
            f_script.write("\n")

        print "%s is generated" % self.scriptName
        print "source %s >&%s.log" % (self.scriptName, self.scriptName.split(".sh")[0])

        f_script.close()

        # -- clear
        self.List_CMD = []

    def Register(self):
        self.MakeCMD()
        self.Clear()


    def MakeCMD(self):
        inputMC_noExt = self.inputMC.split(".root")[0]
        inputMC_type = self.inputMC.split(".root")[0].split("/")[-1]

        CMD = """
root -l -b -q \\
{inputMC_} \\
{inputData_} \\
{reweightCode_}++

mv {inputMC_noExt_}_WithWeights.root \\
{outputMC_}

mv nVtx.png nVtx_{inputMC_type_}.png

echo "Reweight of {inputMC_}: finished"
echo "  -> output file = {outputMC_}"

""".format(inputMC_ = self.inputMC, inputData_ = self.inputData, 
           inputMC_noExt_ = inputMC_noExt, outputMC_ = self.outputMC,
           reweightCode_ = self.reweightCode, inputMC_type_ = inputMC_type )

        self.List_CMD.append(CMD)


    def Clear(self):
        self.inputData = ""
        self.inputMC = ""
        self.outputMC = ""




