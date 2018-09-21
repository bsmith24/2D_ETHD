# 2D_ETHD
This repository contains the working scripts for running the ETHD methodology in 2D on various model potentials.


The code currently works as follows:

1. The driver of the code is a function called  "run_2D()"
2. Here, we have 3 loops, for model, entanglement_option (ent_opt), and case (p0 = 3, p0 = 4)
3. Details for each model and case are found in the funciton "init_params". In this function, the user will define what the model and case will be. 
4. run_2D() then calls run_QC(), for a specific model, ent_opt, and case combination. (QC = Quantum Classical). Quantum will be soon implimented in this script.

Some examples are as follows:

EXAMPLE 1:

def run2D():
    for model in [1]:
        for ent_opt in [0]:
            for case in [0,1]:

                params = init_params(model, case)
                run_test(Nsnaps, Nsteps, params, case, ent_opt)


In this example (EXAMPLE 1), passed to init_params(model, case) is model = 1 and case = 0. This would correspond to the following in the init_params() fucntion:
    if model == 1:
        # Martens' model I
        if case == 0:
            params.update({"model":1, "q0":-1.0, "q1":0.0, "p0":3.0, "p1":0.0, "sq0":0.25, "sq1":0.25, "sp0":0.0,  "sp1":0.0})

Now that our params dictionary is made and updated, we now being our simulaiton using this specific model and case. ent_opt = 0 corresponds to  classical simulation.
The output file titlels "output" will appear as follows: _output_XYZ, where X = model, Y = ent_opt, and Z = case. 

EXAMPLE 2:
def run2D():
    for model in [1,2]:
        for ent_opt in [0,1]:
            for case in [0,1]:

                params = init_params(model, case)
                run_test(Nsnaps, Nsteps, params, case, ent_opt)

In this exmaple (EXAMPLE 2), we study both of Martens' models, with both classical and ETHD methodologies, and examine 2 cases where the initial momentum is different. 
