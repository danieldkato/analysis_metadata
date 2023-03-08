# Last updated DDK 2023-03-07.

import sys
import os
import subprocess
import json

class Metadata:
    """
    Class for storing metadata related to analysis or processing job.

    Attributes
    -----------
    inputs: list
        List of dicts, each corresponding to one input file used in the analysis
        associated with the metadata object. Each dict defines a 'path' key by 
        default. Running write_metadata() additionally adds a 'sha1' key to 
        each dict with the sha1 checksum of the corresponding input file.
    
    outputs: list
        List of dicts, each corresponding to one output file generated by the 
        analysis associated with the metadata object. Each dict defines a 
        'path' key by default. Running write_metadata() additionally adds a 
        'sha1' key to each dict with the sha1 checksum of the corresponding 
        output file.

    parameters: dict
        Dict of parameters used in job associated with metadata. Initialized as
        empty list.

    date: str
        Date job associated with metadata completed.

    time: str
        Time job associated with metadata completed.


    Methods
    --------
    add_input(path):
        Add dict to self.inputs. Initialized just with file path.

    add_output(path):
        Add dict to self.outputs. Initialized just with file path. 
    """

    def __init__(self):            
        self.inputs=[]
        self.outputs=[]
        self.parameters=dict()
        self.date=None
        self.time=None

    def add_input(self, path):
    #Add input file path to self.dict["inputs"].
        d = {"path":path}
        self.inputs.append(d)

    def add_output(self,path):
    #Add output file path to self.dict["outputs"].
        d = {"path":path}
        self.outputs.append(d)
        
    def add_param(self, key, value):
        self.parameters[key] = value

        

def write_metadata(Metadata, fname, debug=False):
    """
    Write metadata associated with given analysis or processing job to secondary
    storage as JSON file. 

    Parameters
    ----------
    Metadata: analysis_metdata.analysis_metadata.Metadata 
    	Metadata object containing job-associated metadata to be saved to
        secondary storage.

    fname: str
        Path to JSON file where metadata should be saved. 

    """ 

    # Get SHA1 checksums of all input and output files: 
    io = [Metadata.inputs, Metadata.outputs] 
    for file_list in io:
        for j, f in enumerate(file_list):
            if 'sha1' not in f:
                if not debug:
                    print('Computing checksum for ' + f["path"] + '...')
                    checksum = get_sha1(f["path"])
                    py_ver = sys.version_info
                    if py_ver.major > 2:
                        checksum = checksum.decode('utf-8') 
                elif debug:
                    checksum = 'test' 
                f["sha1"] = checksum  
    # TODO: try to get software version information

    # Write object to json:
    final_dict={
        'inputs' : Metadata.inputs,
        'parameters' : Metadata.parameters,
        'outputs' : Metadata.outputs,
        'date' : Metadata.date,
        'time' : Metadata.time
        }
    if fname is not None:
        with open(fname, 'w') as outfile:
            json.dump(final_dict, outfile, indent=4)

    # Formally return Metadata object, which now includes input file checksums:
    return Metadata
        


def get_sha1(path):
    
    if os.name == 'posix':
        cmd = ['sha1sum', path]
    elif os.name == 'nt':
        cmd = ['fciv.exe', path, '-sha1']

    sys_out = subprocess.check_output(cmd) 

    if os.name == 'posix':
        sha1 = sys_out[0:40]
    elif os.name == 'nt':
        sha1_end = len(sys_out) - len(path) - 3
        sha1_start = sha1_end - 40
        sha1 = sys_out[sha1_start:sha1_end]
    
    return sha1
