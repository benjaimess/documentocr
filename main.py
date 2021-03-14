import os,pathlib,re,shutil,argparse
import ocrmypdf
import tempfile



def check_path_valid(PATH:pathlib.Path):
    if not (PATH.is_file() and PATH.suffix == '.pdf') and (not PATH.is_dir()):
        raise print(f'  only accept folder or pdf file ')

    elif (PATH.is_file() and PATH.suffix == '.pdf'):
      #  print(f' pdf file path : {PATH}')
        return 'file'
    else:
       # print(f' input folder path : {PATH}')
        return 'folder'


def pdf_extraction_func(pdf_file_path:pathlib.Path,output_folder_path:pathlib.Path, ):
        temp_folder= tempfile.TemporaryDirectory()
        temp_foldername =temp_folder.name
        filename_no_suffix=re.sub('__|___|____','_',re.sub('\s|\.|\-','_', pdf_file_path.stem))

        pdf_file_temp_path= pathlib.Path(temp_foldername) / (filename_no_suffix + pdf_file_path.suffix)

        shutil.copy(pdf_file_path, pdf_file_temp_path)

        pdf_txt_temp_path= pathlib.Path(temp_foldername)  / (filename_no_suffix + '.txt')
        pdf_modified_file_path = pathlib.Path(temp_foldername)  / (filename_no_suffix + '_modified.pdf')

        ocrmypdf.ocr(input_file=pdf_file_temp_path,sidecar=pdf_txt_temp_path,output_file=pdf_modified_file_path,language='eng+chi_tra',optimize=3, deskew=True,force_ocr=True,progress_bar=True,image_dpi=1200,tesseract_oem=1, tesseract_pagesegmode=3)

        with open(pdf_txt_temp_path, 'r', encoding='utf-8') as f:
            lines=[line  for line in f.readlines() if len(line.strip().strip('\n'))>1 ]


        pdf_txt_path = output_folder_path / (pdf_file_path.stem + '.txt')

        with open(pdf_txt_path, 'w', encoding='utf-8') as g:
            for line in lines:
                g.write(line)

        temp_folder.cleanup()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, type=str, help="intput directory")
    parser.add_argument('-o', '--output', required=True,type=str,   help="output directory")

    args = parser.parse_args()



    output_path =pathlib.Path(args.output)
    input_path=pathlib.Path(args.input)

    # output_path=pathlib.Path(r'C:\Users\marcus\PycharmProjects\untitled\pdf_extraction')
    # input_path=pathlib.Path(r'C:\Users\marcus\PycharmProjects\untitled\Data\Leasing Training Dataset - 1\20210209\Leasing\101. DGTE LABORATORY LTD')

    input_path_check=check_path_valid(input_path)
    output_path_check=check_path_valid(output_path)

    if input_path_check =='folder' and output_path_check=='file':
        raise print(f' input path {input_path} is folder and output path {output_path} cannot be file , please check if output  path should be {output_path.parent}')
    elif input_path_check =='file' and output_path_check=='file':
        output_path=output_path.parent
    elif input_path_check=='folder' and output_path_check=='folder' :
        #print(f'success : input path {input_path} is folder and output path {output_path} is folder')
        output_folder_path=output_path/input_path.name
        output_folder_path.mkdir(parents=False,exist_ok=True)
        pdf_files = input_path.glob("*.pdf")
        for pdf_file_path in pdf_files:
            pdf_extraction_func(pdf_file_path=pdf_file_path, output_folder_path=output_folder_path)
        #     for pdf_sample_path in pdf_files:
    elif input_path_check == 'file' and output_path_check == 'folder':
        #print(f'success : input path {input_path} is file and output path {output_path} is folder')
        pdf_extraction_func(pdf_file_path=input_path, output_folder_path=output_path)
    else:
        raise print(f' input path {input_path}  and output path {output_path} also got problem')


