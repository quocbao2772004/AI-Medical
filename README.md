# AI - Medical

<h3>Tutorial for creating real Xray from public dataset lidc-idri</h3>

Creating X-ray images from public [dataset lidc-idri ]([url](https://www.cancerimagingarchive.net/collection/lidc-idri/))

Using DiffDRR to create DRR images from LIDC-IDRI:

    git clone https://github.com/eigenvivek/DiffDRR.git
    git clone https://github.com/quocbao2772004/gs.git
    
Open folder process_dicom_file to see 3 functions to process data from these public dataset and use them to create DRR images.

Example: 

![LIDC-IDRI-0006](https://github.com/user-attachments/assets/317fb3c1-f54d-4e04-ad8e-800f6e53184c)
![LIDC-IDRI-0005](https://github.com/user-attachments/assets/7ba9efb7-3b9a-401d-ba93-80c6ed2e8c07)
![LIDC-IDRI-0004](https://github.com/user-attachments/assets/b2d6c2ff-348e-4955-a47f-42178d0b1530)
![LIDC-IDRI-0003](https://github.com/user-attachments/assets/9d394d9d-294a-4774-be1a-4cffbe6ccee7)
![LIDC-IDRI-0002](https://github.com/user-attachments/assets/a045a29d-9d74-46d1-b811-a704ae7df390)
![LIDC-IDRI-0001](https://github.com/user-attachments/assets/c2c6ada0-7335-4599-96fa-a24d98e63edd)

Using CycleGan to mapping DRR images to real X-rays images

    git clone https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.git

After cloning, please download this pretrained model for maping to real X-rays images [link](https://drive.google.com/drive/folders/1_Ih11XM8CEYkP45nUgPXu8_3KhY25uMZ?usp=drive_link)

Example:

![LIDC-IDRI-0002_fake_B](https://github.com/user-attachments/assets/f688ab0a-41f5-4898-8cf6-13c08088afd1)
![LIDC-IDRI-0001_fake_B](https://github.com/user-attachments/assets/6cc54743-6f9e-4c1c-bbe6-c0699653a64b)
![LIDC-IDRI-0006_fake_B](https://github.com/user-attachments/assets/626c279f-a901-4e5d-9648-12b328d05447)
![LIDC-IDRI-0005_fake_B](https://github.com/user-attachments/assets/457e47bf-88ab-4e25-bc6c-964b852719ab)
![LIDC-IDRI-0004_fake_B](https://github.com/user-attachments/assets/59d249f1-93af-4917-9304-8b3eedc82557)
![LIDC-IDRI-0003_fake_B](https://github.com/user-attachments/assets/5fb7db5f-a01d-4445-a291-763746543f48)
