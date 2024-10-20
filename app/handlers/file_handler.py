import os
import tempfile
import shutil
import zipfile

class FileHandler:
    def create_temp_folder(self) -> str:
        temp_dir = tempfile.mkdtemp()
        return temp_dir

    def save_local_file(self, filename: str, content: str, folder: str) -> str:
        #Salva um arquivo localmente dentro da pasta especificada.
        file_path = os.path.join(folder, filename)
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File saved at: {file_path}")
        return file_path

    def zip_folder(self, folder_path: str, output_filename: str):
        #Compacta uma pasta inteira em um arquivo zip.
        with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=folder_path)  # Preserva a estrutura de diretórios
                    zip_file.write(file_path, arcname=arcname)
        print(f"Folder zipped to: {output_filename}")
    
    def clear_dir(self, folder: str):
        #Remove um diretório e todo o seu conteúdo.
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Folder {folder} deleted.")
        else:
            print(f"Folder {folder} not found.")