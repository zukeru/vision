#!/usr/bin/python

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

        packerfile = json_file
        exc = []        
        #only = ['my_first_image', 'my_second_image']
        packer_exec_path = 'packer'
        print 'Starting Packer Build...'
        p = packer.Packer(packerfile,exec_path=packer_exec_path)

        try:
            out = p.build(parallel=True, debug=False, force=False)
            print out.stdout    
        except Exception as e:
            print e.stdout    
    
    output = execute_packer_vbox_build(json_file, config_file)
    print output

    output = execute_packer_vbox_build(json_file, config_file)
    print output


ssh_name = '        "ssh_name": "test",\n'
ssh_pass = '        "ssh_pass": "test",\n'
hostname = '        "hostname": "packer-test"\n'
builder_type = '        "type": "virtualbox-iso",\n'
guest_os_type = '        "guest_os_type": "Ubuntu_64",\n'
modifyvm = '            ["modifyvm", "{{.Name}}", "--vram", "32"]\n'
disk_size = '        "disk_size" : 10000,\n'
iso_url = '        "iso_url": "http://releases.ubuntu.com/14.04.2/ubuntu-14.04.2-server-amd64.iso",\n'
iso_checksum = '        "iso_checksum": "83aabd8dcf1e8f469f3c72fff2375195",\n'
iso_checksum_type = '        "iso_checksum_type": "md5",\n'
http_directory = '        "http_directory" : "ubuntu_64",\n'
http_port_min = '        "http_port_min" : 9001,\n'
http_port_max = '        "http_port_max" : 9001,\n'
ssh_wait_timeout = '        "ssh_wait_timeout": "20m",\n'

boot_commands = ['            "<esc><esc><enter><wait>",\n',
                 '            "/install/vmlinuz noapic ",\n',
                 '            "preseed/url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/preseed.cfg ",\n',
                 '            "debian-installer=en_US auto locale=en_US kbd-chooser/method=us ",\n',
                 '            "hostname={{user `hostname`}} ",\n',
                 '            "fb=false debconf/frontend=noninteractive ",\n',
                 '            "keyboard-configuration/modelcode=SKIP keyboard-configuration/layout=USA ",\n',
                 '            "keyboard-configuration/variant=USA console-setup/ask_detect=false ",\n',
                 '            "initrd=/install/initrd.gz -- <enter>"\n' ]
def write_vitualbox(file,file_config,directory_file,ssh_name,ssh_pass,hostname,builder_type,guest_os_type,modifyvm,disk_size,iso_url,iso_checksum,iso_checksum_type,http_directory,http_port_min,http_port_max,ssh_wait_timeout, boot_commands):
    import json
    
    print "Building Packer Configs..."
    file.write('{\n')
    file.write('    "variables": {\n')
    file.write(ssh_name)
    file.write(ssh_pass)
    file.write(hostname)
    file.write('    },\n')
    file.write('\n ')
    file.write('    "builders": [{\n')
    file.write(builder_type)
    file.write(guest_os_type)
    file.write('\n ')
    file.write('        "vboxmanage": [\n')
    file.write(modifyvm)
    file.write('        ],\n')
    file.write('\n ')
    file.write(disk_size)
    file.write('\n ')
    file.write(iso_url)
    file.write(iso_checksum)
    file.write(iso_checksum_type)
    file.write(' ')
    file.write(http_directory)
    file.write(http_port_min)
    file.write(http_port_max)
    file.write('        "ssh_username": "{{user `ssh_name`}}",\n')
    file.write('        "ssh_password": "{{user `ssh_pass`}}",\n')
    file.write(ssh_wait_timeout)
    file.write(' ')
    file.write('        "shutdown_command": "echo {{user `ssh_pass`}} | sudo -S shutdown -P now",\n')
    file.write('\n ')
    file.write('        "boot_command" : [\n')
    for command in boot_commands:
        file.write(command)
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
    
    '''
    file = open(directory_file, 'r')
    lines = file.read()
    json_conv = json.loads(str(lines))
    json_output_str = json.dumps(json_conv)
    file.close()
    file = open(directory_file, 'w')
    file.write(json_output_str)
    file.close()
    '''
filename = str(uuid.uuid4())
mkdir_p(filename)

directory_file = (os.path.dirname(os.path.realpath(__file__)) + '/' + filename + "/build-file_" + filename + '.json')
directory_file_path = (os.path.dirname(os.path.realpath(__file__)) + '/' + filename + "/config_" + filename + '.cfg')


file_config = open(directory_file_path , 'w')
file = open(directory_file, 'w')
write_vitualbox(file,file_config,directory_file,ssh_name,ssh_pass,hostname,builder_type,guest_os_type,modifyvm,disk_size,iso_url,iso_checksum,iso_checksum_type,http_directory,http_port_min,http_port_max,ssh_wait_timeout, boot_commands)
execute_build(directory_file, directory_file_path)



#only = ['my_first_image', 'my_second_image']
#vars = {"variable1": "value1", "variable2": "value2"}
#vars_file = config_file
#p = packer.Packer(packerfile, exc=exc, only=only, vars=vars,
#vars_file=vars_file, exec_path=packer_exec_path)