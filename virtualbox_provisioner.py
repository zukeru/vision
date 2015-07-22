import uuid
import os, errno
import subprocess
import packer

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
        
def execute_build(json_file, config_file):
    def execute_packer_vbox_build(json_file, config_file):
        import packer

        p = packer.Installer('~/packer', '0.6.1_linux_amd64.zip')
        packer_exec = p.install()
        packerfile = json_file
        exc = []
        only = ['my_first_image', 'my_second_image']
        vars = {"variable1": "value1", "variable2": "value2"}
        vars_file = config_file
        packer_exec_path = 'packer'
        
        p = packer.Packer(packerfile, exc=exc, only=only, vars=vars,
                          vars_file=vars_file, exec_path=packer_exec_path)
        p.build(parallel=True, debug=False, force=False)
        
    
    output = execute_packer_vbox_build(json_file, config_file)
    print output

    output = execute_packer_vbox_build(json_file, config_file)
    print output

def write_vitualbox(file, file_config):
    file.write('{\n')
    file.write('    "variables": {\n')
    file.write('        "ssh_name": "kappataumu",\n')
    file.write('        "ssh_pass": "kappataumu",\n')
    file.write('        "hostname": "packer-test"\n')
    file.write('    },\n')
    file.write('\n ')
    file.write('    "builders": [{\n')
    file.write('        "type": "virtualbox-iso",\n')
    file.write('        "guest_os_type": "Ubuntu_64",\n')
    file.write('\n ')
    file.write('        "vboxmanage": [\n')
    file.write('            ["modifyvm", "{{.Name}}", "--vram", "32"]\n')
    file.write('        ],\n')
    file.write('\n ')
    file.write('        "disk_size" : 10000,\n')
    file.write('\n ')
    file.write('        "iso_url": "http://releases.ubuntu.com/precise/ubuntu-12.04.3-server-amd64.iso",\n')
    file.write('        "iso_checksum": "2cbe868812a871242cdcdd8f2fd6feb9",\n')
    file.write('        "iso_checksum_type": "md5",\n')
    file.write(' ')
    file.write('        "http_directory" : "ubuntu_64",\n')
    file.write('        "http_port_min" : 9001,\n')
    file.write('        "http_port_max" : 9001,\n')
    file.write('        "ssh_username": "{{user `ssh_name`}}",\n')
    file.write('        "ssh_password": "{{user `ssh_pass`}}",\n')
    file.write('        "ssh_wait_timeout": "20m",\n')
    file.write(' ')
    file.write('        "shutdown_command": "echo {{user `ssh_pass`}} | sudo -S shutdown -P now",\n')
    file.write('\n ')
    file.write('        "boot_command" : [\n')
    file.write('            "<esc><esc><enter><wait>",\n')
    file.write('            "/install/vmlinuz noapic ",\n')
    file.write('            "preseed/url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/preseed.cfg ",\n')
    file.write('            "debian-installer=en_US auto locale=en_US kbd-chooser/method=us ",\n')
    file.write('            "hostname={{user `hostname`}} ",\n')
    file.write('            "fb=false debconf/frontend=noninteractive ",\n')
    file.write('            "keyboard-configuration/modelcode=SKIP keyboard-configuration/layout=USA ",\n')
    file.write('            "keyboard-configuration/variant=USA console-setup/ask_detect=false ",\n')
    file.write('            "initrd=/install/initrd.gz -- <enter>"\n')
    file.write('        ]\n')
    file.write('    }]\n')
    file.write('}\n')
    
    file_config.write('# Some inspiration:\n')
    file_config.write('# * https://github.com/chrisroberts/vagrant-boxes/blob/master/definitions/precise-64/preseed.cfg\n')
    file_config.write('# * https://github.com/cal/vagrant-ubuntu-precise-64/blob/master/preseed.cfg\n')
    
    file_config.write('# English plx\n')
    file_config.write('d-i debian-installer/language string en\n')
    file_config.write('d-i debian-installer/locale string en_US.UTF-8\n')
    file_config.write('d-i localechooser/preferred-locale string en_US.UTF-8\n')
    file_config.write('d-i localechooser/supported-locales en_US.UTF-8\n')
    
    file_config.write('# Including keyboards\n')
    file_config.write('d-i console-setup/ask_detect boolean false\n')
    file_config.write('d-i keyboard-configuration/layout select USA\n')
    file_config.write('d-i keyboard-configuration/variant select USA\n')
    file_config.write('d-i keyboard-configuration/modelcode string pc105\n')
    
    
    file_config.write('# Just roll with it\n')
    file_config.write('d-i netcfg/get_hostname string this-host\n')
    file_config.write('d-i netcfg/get_domain string this-host\n')
    
    file_config.write('d-i time/zone string UTC\n')
    file_config.write('d-i clock-setup/utc-auto boolean true\n')
    file_config.write('d-i clock-setup/utc boolean true\n')
    
    
    file_config.write('# Choices: Dialog, Readline, Gnome, Kde, Editor, Noninteractive\n')
    file_config.write('d-i debconf debconf/frontend select Noninteractive\n')
    
    file_config.write('d-i pkgsel/install-language-support boolean false\n')
    file_config.write('tasksel tasksel/first multiselect standard, ubuntu-server\n')
    
    file_config.write('# Stuck between a rock and a HDD place\n')
    file_config.write('d-i partman-auto/method string lvm\n')
    file_config.write('d-i partman-lvm/confirm boolean true\n')
    file_config.write('d-i partman-lvm/device_remove_lvm boolean true\n')
    file_config.write('d-i partman-auto/choose_recipe select atomic\n')
    
    file_config.write('d-i partman/confirm_write_new_label boolean true\n')
    file_config.write('d-i partman/confirm_nooverwrite boolean true\n')
    file_config.write('d-i partman/choose_partition select finish\n')
    file_config.write('d-i partman/confirm boolean true\n')
    
    file_config.write('# Write the changes to disks and configure LVM?\n')
    file_config.write('d-i partman-lvm/confirm boolean true\n')
    file_config.write('d-i partman-lvm/confirm_nooverwrite boolean true\n')
    file_config.write('d-i partman-auto-lvm/guided_size string max\n')
    
    file_config.write('# No proxy, plx\n')
    file_config.write('d-i mirror/http/proxy string\n')
    
    file_config.write('# Default user, change\n')
    file_config.write('d-i passwd/user-fullname string kappataumu\n')
    file_config.write('d-i passwd/username string kappataumu\n')
    file_config.write('d-i passwd/user-password password kappataumu\n')
    file_config.write('d-i passwd/user-password-again password kappataumu\n')
    file_config.write('d-i user-setup/encrypt-home boolean false\n')
    file_config.write('d-i user-setup/allow-password-weak boolean true\n')
    
    file_config.write('# No language support packages.\n')
    file_config.write('d-i pkgsel/install-language-support boolean false\n')
    
    file_config.write('# Individual additional packages to install\n')
    file_config.write('d-i pkgsel/include string build-essential ssh\n')
    
    file_config.write('#For the update\n')
    file_config.write('d-i pkgsel/update-policy select none\n')
    
    file_config.write('# Whether to upgrade packages after debootstrap.\n')
    file_config.write('# Allowed values: none, safe-upgrade, full-upgrade\n')
    file_config.write('d-i pkgsel/upgrade select safe-upgrade\n')
    
    file_config.write('# Go grub, go!\n')
    file_config.write('d-i grub-installer/only_debian boolean true\n')
    
    file_config.write('d-i finish-install/reboot_in_progress note\n')
    
    file_config.close()
    file.close()


filename = str(uuid.uuid4())
mkdir_p(filename)

directory_file = (os.path.dirname(os.path.realpath(__file__)) + '/' + filename + "/build-file_" + filename + '.json')
directory_file_path = (os.path.dirname(os.path.realpath(__file__)) + '/' + filename + "/config_" + filename + '.cfg')


file_config = open(directory_file_path , 'w')
file = open(directory_file, 'w')
write_vitualbox(file, file_config)
execute_build(directory_file, directory_file_path)