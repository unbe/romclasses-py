romclasses-py
=============

**** HACK *** HACK *** HACK *** HACK ****

This is an attempt to parse IBM J9 Java VM's rom.classes files in python. Although it does parse the general structure, locate the classes and methods and displays their names, a lot of features are missing, such as displaying constants (e.g. strings) and dumping the actual bytecode. Since this is a development version, a lot of unnecessary internal information and structures are parsed and printed.

I hope one day I will have time and will to reverse engineer the rest of it.

Check out my romclasses-c repo for a different approach to parsing rom.classes.

NOTE: If your rom.classes file is large, this will take a long time to run and the ouput will be **huge**. 


```
$ python dumpjxe.py rom.classes | head -n 50
Container:
    signature = 'CORRECT'
    flags_and_version = 101255430
    rom_size = 27074968
    class_count = 6036
    jxe_pointer = -48
    toc_pointer = 48
    first_class_pointer = 3275552
    aot_pointer = None
    symbol_file_id = [
        160
        176
        62
        80
        255
        105
        17
        226
        128
        54
        129
        64
        88
        165
        185
        181
    ]
    J9ROMClassTOCEntry = [
        Container:
            class_name = 'java/io/File'
            class_pointer = 3563320
            J9ROMClass = Container:
                rom_size = 8880
                single_scalar_static_count = 4
                class_name = 'java/io/File'
                superclass_name = 'java/lang/Object'
                modifiers = 33
                interface_count = 2
                interfaces_pointer = 3564940
                rom_method_count = 73
                rom_methods_pointer = 3566792
                rom_field_count = 9
                rom_fields_pointer = 3564824
                object_static_count = 2
                double_scalar_static_count = 1
                ram_constant_pool_count = 173
                rom_constant_pool_count = 175
                crc = 0
                instance_size = 8
                instance_shape = 14
      [... lots of output ...]
```

