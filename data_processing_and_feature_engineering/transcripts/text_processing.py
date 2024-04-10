import os
from docx import Document

def convertFromDocxToTxt():
    # Set the source and destination directories
    source_folder = os.path.join("data", "CCM_Transcript_Data", "Transcription")
    destination_folder = os.path.join("data", "CCM_Transcript_Text_Data")

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # List all .docx files in the source folder
    docx_files = [f for f in os.listdir(source_folder) if f.endswith('.docx')]

    # Process each .docx file
    for docx_file in docx_files:
        # Create the full file paths for source and destination
        source_path = os.path.join(source_folder, docx_file)
        destination_path = os.path.join(destination_folder, os.path.splitext(docx_file)[0] + '.txt')
        try:
            # Read the content of the .docx file
            doc = Document(source_path)
            text = '\n'.join([para.text for para in doc.paragraphs])

            #Filtering lines
            lines = [line for line in text.split('\n') if not line.isspace()]
            filtered_lines = [
                line.strip()
                for line in lines
                if not line.startswith('00:')
                and not line.startswith("Audio file")
                and not line.endswith(".mp3")
                and not line.startswith("Transcript")
                and not line.endswith(".m4a")
            ]
            filtered_text = '\n'.join([s for s in filtered_lines if s])

            # Write the content to a text file in the destination folder
            with open(destination_path, 'w', encoding='utf-8') as text_file:
                text_file.write(filtered_text)

            print(f'Converted {docx_file} to {os.path.basename(destination_path)}')

        except Exception as e:
            print(f"Error processing {docx_file}: {e}")

    print("Conversion complete.")

if __name__ == "__main__":
    convertFromDocxToTxt()