import pytest
import tppparser
import subprocess
import shlex
import os, fnmatch

test_cases = [("", "-k"), ("teste.c", "-k")]

for file in fnmatch.filter(os.listdir('tests/'), '*.tpp'):
    test_cases.append((file, "-k"))


@pytest.mark.parametrize("input_file, args", test_cases)
def test_execute(input_file, args):
    if(input_file != ''):
        path_file = 'tests/' + input_file
    else:
        path_file = ""
    
    # Por algum motivo quando passava input_file = "" o pytest passava um nome de arquivo e dava o erro:
    # b'ERR-LEX-NOT-TPP\n'
    # Expected output:
    # ERR-LEX-USE
    # process = subprocess.Popen(['python', 'tpplex.py', args, path_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd = "python tppparser.py {0} {1}".format(args, path_file)
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    stdout, stderr = process.communicate()
    stdout, stderr

    path_file = 'tests/' + input_file
    output_file = open(path_file + ".syn.out", "r")

    #read whole file to a string
    expected_output = output_file.read()

    output_file.close()

    print("Generated output:")
    print(stdout)
    print("Expected output:")
    print(expected_output)

    assert stdout.decode("utf-8") == expected_output


