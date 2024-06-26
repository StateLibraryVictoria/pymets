import os
import shutil

from lxml import etree as ET
from pytest import *

from pymets import mets_factory as mf

nsmap = {"dnx"}

mixed_files = ['1.txt', '2.txt', 'apples.txt', 'carrots.txt', 'zebras.txt',
               '99.txt', 'aarvarks.txt', '4.txt']

def setup_function():
    print("SETUP!")
    if not os.path.exists('manyfiles_numeric'):
        os.mkdir('manyfiles_numeric')
        for i in range(100):
            i = str(i)
            with open('manyfiles_numeric/{}.txt'.format(i), 'w') as f:
                f.write(i)
    if not os.path.exists('manyfiles_alphanum'):
        os.mkdir('manyfiles_alphanum')
        for i in range(100):
            i = str(i)
            with open('manyfiles_alphanum/page {}.txt'.format(i), 'w') as f:
                f.write(i)
    if not os.path.exists('manyfiles_mixed'):
        os.mkdir('manyfiles_mixed')
        for i in mixed_files:
            with open('manyfiles_mixed/{}'.format(i), 'w') as f:
                f.write(i)
    if not os.path.exists('manyfiles_leading_zeroes'):
        os.mkdir('manyfiles_leading_zeroes')
        for i in range(100):
            filename = 'page {:02d}.txt'.format(i)
            with open('manyfiles_leading_zeroes/{}'.format(filename), 'w') as f:
                f.write(filename)

def teardown_function():
    print("TEAR DOWN!")
    shutil.rmtree('manyfiles_numeric')
    shutil.rmtree('manyfiles_alphanum')
    shutil.rmtree('manyfiles_mixed')
    shutil.rmtree('manyfiles_leading_zeroes')

def test_basic():
    print("I ran!")

def test_build_amdsec_filegrp_structmap():
    mets = mf.build_mets()
    mf.build_amdsec_filegrp_structmap(mets,
        ie_id='ie1',
        pres_master_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_1',
                'pm'),
        modified_master_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_1',
                'mm'),
        access_derivative_dir=None,
        digital_original=False,
        input_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_1'))
    amd_sec_list = mets.findall("./{http://www.loc.gov/METS/}amdSec")
    print("Here is the list of amdSec items: {}".format(amd_sec_list))
    assert(len(amd_sec_list) == 4)
    print(ET.tostring(mets, pretty_print=True))

def test_ordered_numeric_file_list():
    """make sure that numeric values are returned in a sensible order"""
    filelist = mf.ordered_file_list('manyfiles_numeric')
    for i in range(100):
        str_i = str(i)
        assert(filelist[i] == os.path.join('manyfiles_numeric','{}.txt'.format(str_i)))
    # assert(filelist[0] == 'manyfiles_numeric/0.txt')
    # assert(filelist[-1] == 'manyfiles_numeric/99.txt')
    print(filelist)

def test_ordered_alphanum_file_list():
    """non-numeric filenames should return like sorted(os.listdir())"""
    filelist = mf.ordered_file_list('manyfiles_alphanum')
    test_list = []
    for i in range(100):
        test_list.append(os.path.join('manyfiles_alphanum','page {}.txt'.format(str(i))))
    test_list = sorted(test_list)
    assert(test_list == filelist)
    # assert(filelist[0] == 'manyfiles_alphanum/page 0.txt')
    # assert(filelist[-1] == 'manyfiles_alphanum/page 99.txt')
    print(filelist)

def test_mixed_numeric_alphanum_files():
    """alphanum files should appear first and sorted, then sorted numeric files"""
    test_list = ['manyfiles_mixed/aarvarks.txt', 'manyfiles_mixed/apples.txt',
                 'manyfiles_mixed/carrots.txt', 'manyfiles_mixed/zebras.txt',
                 'manyfiles_mixed/1.txt', 'manyfiles_mixed/2.txt',
                 'manyfiles_mixed/4.txt', 'manyfiles_mixed/99.txt']
    better_test_list = [os.path.join(*file.split("/")) for file in test_list]
    filelist = mf.ordered_file_list('manyfiles_mixed')
    print(filelist)
    print(better_test_list)
    assert(filelist == better_test_list)


def test_alpahnum_files_with_nums_and_leading_zeroes():
    """files like "page 001.txt" should return like sorted(os.listdir())"""
    filelist = mf.ordered_file_list('manyfiles_leading_zeroes')
    test_list = []
    for test_file in os.listdir('manyfiles_leading_zeroes'):
        test_list.append(os.path.join('manyfiles_leading_zeroes', test_file))
    print(filelist)
    assert(filelist == sorted(test_list))


def test_build_digiprovMD():
    """buld_digiprovMD() function returns a digiprovMD object"""
    xmldata = ET.fromstring(
        "<node><key1>value1</key1><key2>value2</key2></node>")
    mdwrap_obj = mf.build_mdWrap({"MDTYPE": "OTHER", "OTHERMDTYPE": "TEST"},
                                 binData_list=None,
                                 xmlData_list=[xmldata, ])
    print(ET.tostring(mdwrap_obj))
    assert(mdwrap_obj.tag == "{http://www.loc.gov/METS/}mdWrap")


def test_build_amdsec_filegrp_structmap_with_access_dir():
    mets = mf.build_mets()
    mf.build_amdsec_filegrp_structmap(mets,
        ie_id='ie1',
        pres_master_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_1',
                'pm'),
        modified_master_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_1',
                'mm'),
        access_derivative_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_1',
                'mm'),
        digital_original=False,
        input_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_1'))
    amd_sec_list = mets.findall("./{http://www.loc.gov/METS/}amdSec")
    print("Here is the list of amdSec items: {}".format(amd_sec_list))
    assert(len(amd_sec_list) == 6)
    print("now printing a thing...")
    print(ET.tostring(mets, pretty_print=True))
