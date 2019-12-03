import configparser as im_configparser

class ConfigManager():
    """manage config file"""

    def __init__(self, config_path : str):
        """
        initial the config file manager

        :args:
         - config_path: the file path of the config file
        """

        # load config file
        self.config_path = config_path
        self.config = im_configparser.ConfigParser()
        self.config.read(config_path, encoding = 'utf-8-sig')

        return

    def retrieve_key_value(self, section : str, key : str, value_type : int):
        """
        retrieve key value by key from specific section

        :args:
         - section: section name
         - key: key name
         - value_type: the type of key value
           0: int
           1: str
        """
        # return, if the section or the key is not exist

        if not self.config.has_section(section): return
        if not self.config.has_option(section, key): return

        # retrieve key value
        if value_type == 0:
            return self.config.getint(section, key)
        else: 
            return self.config.get(section, key)

    def update_key_value(self, section : str, key : str, value : str):
        """
        update key value by key under specific section

        :args:
         - section: section name
         - key: key name
         - value: key value
        """

        # return, if the section or the key is not exist
        if not self.config.has_section(section): return
        if not self.config.has_option(section, key): return
    
        # update key value
        self.config.set(section, key, value)
        with open(self.config_path, 'w') as config_file_obj:
            self.config.write(config_file_obj)
            
        return

    def create_key(self, section : str, key : str, value : str):
        """
        create key value under specific section

        :args:
         - section: section name
         - key: key name
         - value: key value
        """

        # return, if the section is not exist, or the key is exist
        if not self.config.has_section(section): return
        if self.config.has_option(section, key): return

        # creat key & value
        self.config.set(section, key, value)
        with open(self.config_path, 'w') as config_file_obj:
            self.config.write(config_file_obj)

        return

    def create_section(self, section : str):
        """
        create section

        :args:
         - section: section name
        """

        # return, if the section is exist
        if self.config.has_section(section): return

        # creat section
        self.config.add_section(section)
        with open(self.config_path, 'w') as config_file_obj:
            self.config.write(config_file_obj)
            
        return