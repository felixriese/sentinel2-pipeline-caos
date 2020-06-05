#
#  taken from:
#    https://gist.github.com/luiscape/19d2d73a8c7b59411a2fb73a697f5ed4#file-install_packages-sh
#

#
#  Install via `conda` directly.
#  This will fail to install all
#  dependencies. If one fails,
#  all dependencies will fail to install.
#
#conda install --yes --file dependencies.txt

#
#  To go around issue above, one can
#  iterate over all lines in the
#  requirements.txt file.
#

case "$OSTYPE" in
  darwin*) while read dependency; do 
        conda install --yes $dependency
        echo $dependency
    done < dependencies/dependencies_macos.txt;; 
  linux*)  while read dependency; do 
        conda install --yes $dependency
        echo $dependency
    done < dependencies/dependencies_linux.txt;;
esac

git clone https://github.com/philipp01wagner/esa_sentinel.git

cp -R ./esa_sentinel/sentinel_api .
rm -rf ./esa_sentinel

touch account.ini
echo '[account_data]' > account.ini

while true; do
    read -p "Do you want to enter your SciHub username and password to download Seninel2 data?" yn
    case $yn in
        [Yy]* ) read -p 'username: ' uservar; read -sp 'password: ' passvar; echo "username=$uservar" >> account.ini; echo "password=$passvar" >> account.ini; break;;
        [Nn]* ) echo 'You can set username and password in the file account.ini.'; echo 'username=' >> account.ini; echo 'password=' >> account.ini; echo ' '; exit;;
        * ) echo "Please answer y or n.";;
    esac
done

chmod +x fuse_resolutions.sh
