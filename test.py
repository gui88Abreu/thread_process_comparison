#!/usr/bin/env python3

#*********************************************************************************************************#
                                              #***import librarys***#

from os import system #execute commands on command line
import sys #catch arguments from the command line that runs this script
import re #RegEx

#*********************************************************************************************************#
                                              #***function statements***#

def yield_table(time_file, Name, test_list, mode):
  ''' 
  Yield a csv table with datas that were colected and stored on time_file.
  String *Name must have something about the datas, example: Thread Method or just Thread.
  '''
  #Store all datas yielded previously in make_test on a list
  file = open(time_file, 'r')
  line = file.readlines()
  file.close()

  #Erase time_file
  system('rm -f ' + time_file)

  # Actually yield a csv table
  planilha = open('Test_Result.csv', mode)
  planilha.write(Name + '\n')
  planilha.write('Test,Width x Height,Real time[s]\n')
  
  regex = re.compile("[0-9]+[.][0-9]+")

  j = 0
  for l in line:
    result = regex.findall(l)
    if len(result) == 1:
      planilha.write(test_list[j] + ',' + l)
      j += 1
  planilha.write('\n')
  planilha.close()

def make_test(test_list, program_target, mode, N_blur, cpu, time_file):
  '''
  It does test program_target with the test_list and store the results on time_file.
  *mode must be assigned with '0' to execute program with threads or with '1' to execute with processes.
  '''
  print(60*'-')
  for i in range(len(test_list)):
    test_list[i] = test_list[i].replace('\n', '')
    print(60*'-')
    print('Test Image: ' + test_list[i])
    system('./'+program_target + ' ' + test_list[i] + ' ' + mode + ' ' + N_blur + ' ' + cpu +  ' >>' + time_file)
  print(60*'-')

#*********************************************************************************************************#
                                              #***main***#



if len(sys.argv) != 2:
  quit('It must be passed as argument just the program name that will be tested')

#File Names
images_directory = "images"
program_target = sys.argv[1]
temp_file = "temp"
time_file = "time"
N_blur = '10'

#Catch the number of available threads of the processor
system('grep -c cpu[0-9] /proc/stat >>' + temp_file)
fl = open(temp_file,'r')
cpu = fl.readline().replace('\n','')
fl.close()

print(80*'-')
print(80*'-')
print('All tests will be done with a blur length of 10.')
print('After that, it will be generated a csv table.')
print('The results that will be taken from the tests will be there.')
print('First it will be executed tests with %s threads.' %cpu)
print('Then it will be executed tests with %s processes.' %cpu)
print('Finally it will be executed test with single processing, i.e, without parallelism.')
print('For bests results, execute this script 2 times and ignore the first.')
print(80*'-')
print(80*'-')

while 1:
  choice  = input('Just type (Y) if you understood or (N) otherwise: ')
  if choice == "N":
    system('rm -f ' + temp_file)
    quit()
  if choice == "Y":
    break

print(80*'-')
print(80*'-')

#Catch all file names in image_directory and store on temp_file
system('ls ' + images_directory + '>' + temp_file)

#Store all names found in image_directory on a list
fl = open(temp_file, 'r')
test_list = fl.readlines()
fl.close()

#Erase temp_file
system('rm -f ' + temp_file)

if len(test_list) == 0:
  quit('There is no test files')

#Run program_target with threads and store the results on time_file
print("Thread Testing")
make_test(test_list, program_target, '0', N_blur, cpu, time_file)
yield_table(time_file, 'Thread', test_list, 'w')

#Run program_target with processes and store the results on time_file
print("Process Testing")
make_test(test_list, program_target, '1', N_blur, cpu,time_file)
yield_table(time_file, 'Process', test_list, 'a')

#Run program_target with processes and store the results on time_file
print("Single Processing Testing")
make_test(test_list, program_target, '-1',N_blur, cpu, time_file)
yield_table(time_file, 'Single Processing', test_list, 'a')
