import os
import shutil

from lxml import etree as ET
import pytest

from pymets import mets_factory as mf

nsmap = {"dnx"}

mixed_files = ['1.txt', '2.txt', 'apples.txt', 'carrots.txt', 'zebras.txt',
               '99.txt', 'aarvarks.txt', '4.txt']

cwd = os.getcwd()
CURRENT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))
data_dir = os.path.join(CURRENT_DIR,"data")

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

def test_ordered_numeric_file_list(tmp_path):
    """make sure that numeric values are returned in a sensible order"""
    print("SETUP")
    d = tmp_path / "manyfiles_numeric"
    d.mkdir()
    for i in range(100):
        i = str(i)
        p = d / f"{i}.txt"
        with open(p, 'w') as f:
            f.write(i)
    filelist = mf.ordered_file_list(d)
    assert(len(filelist)>0)
    for i in range(100):
        str_i = str(i)
        p2 = d / f"{str_i}.txt"
        assert(filelist[i] == os.path.normpath(p2))
    # assert(filelist[0] == 'manyfiles_numeric/0.txt')
    # assert(filelist[-1] == 'manyfiles_numeric/99.txt')
    print(filelist)

def test_ordered_alphanum_file_list(tmp_path):
    """non-numeric filenames should return like sorted(os.listdir())"""
    d = tmp_path / 'manyfiles_alphanum'
    d.mkdir()
    for i in range(100):
        i = str(i)
        p = d / f"page {i}.txt"
        with open(p, 'w') as f:
            f.write(i)
    filelist = mf.ordered_file_list(d)
    test_list = []
    for i in range(100):
        p2 = d / f"page {(str(i))}.txt"
        test_list.append(os.path.normpath(p2))
    test_list = sorted(test_list)
    assert(len(filelist) > 0)
    assert(test_list == filelist)
    # assert(filelist[0] == 'manyfiles_alphanum/page 0.txt')
    # assert(filelist[-1] == 'manyfiles_alphanum/page 99.txt')
    print(filelist)

def test_mixed_numeric_alphanum_files(tmp_path):
    """alphanum files should appear first and sorted, then sorted numeric files"""
    d = tmp_path / 'manyfiles_mixed'
    d.mkdir()
    for i in mixed_files:
        p = d / i
        with open(p, 'w') as f:
            f.write(i)
    test_list = ['manyfiles_mixed/aarvarks.txt', 'manyfiles_mixed/apples.txt',
                 'manyfiles_mixed/carrots.txt', 'manyfiles_mixed/zebras.txt',
                 'manyfiles_mixed/1.txt', 'manyfiles_mixed/2.txt',
                 'manyfiles_mixed/4.txt', 'manyfiles_mixed/99.txt']
    temp_test_list = []
    for item in test_list:
        file = os.path.normpath(tmp_path / item)
        temp_test_list.append(file)
    filelist = mf.ordered_file_list(d)
    print(filelist)
    print(temp_test_list)
    assert(len(filelist)>0)
    assert(filelist == temp_test_list)


def test_alpahnum_files_with_nums_and_leading_zeroes(tmp_path):
    """files like "page 001.txt" should return like sorted(os.listdir())"""
    d = tmp_path / 'manyfiles_leading_zeroes'
    d.mkdir()
    for i in range(100):
        filename = f'page {i:>02}.txt'
        p = d / filename
        with open(p, 'w') as f:
            f.write(filename)
    filelist = mf.ordered_file_list(d)
    test_list = []
    for test_file in os.listdir(d):
        file_path = d / test_file
        test_list.append(os.path.normpath(file_path))
    print(filelist)
    assert(len(filelist) > 0)
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
