import sys

from construct import *

input = open(sys.argv[1], "rb")
data = input.read()
input.close()

def RelativePointer(name):
	return ExprAdapter(Struct(name, Anchor("_base"), SLInt32("_ptr")), 
		encoder = lambda obj, ctx: "",
		decoder = lambda obj, ctx: obj._base + obj._ptr)

J9ROMImageHeader = Struct("J9ROMImageHeader",
	Enum(ULInt32("signature"),
		CORRECT = 1245264202,
		_default_ = Pass,
	),
	ULInt32("flags_and_version"),
	ULInt32("rom_size"),
	ULInt32("class_count"),
	RelativePointer("jxe_pointer"),
	RelativePointer("toc_pointer"),
	RelativePointer("first_class_pointer"),
	RelativePointer("aot_pointer"),
	Array(16, ULInt8("symbol_file_id")),
	Pointer(lambda ctx: ctx.toc_pointer, Array(lambda ctx: ctx.class_count, 
		Struct("J9ROMClassTOCEntry",
			RelativePointer("class_name_pointer"),
			RelativePointer("class_pointer"),
			Pointer(lambda ctx: ctx.class_name_pointer, PascalString("class_name", length_field=ULInt16("length"))),
			Pointer(lambda ctx: ctx.class_pointer, Struct("J9ROMClass",
			    ULInt32("rom_size"),
			    ULInt32("single_scalar_static_count"),
			    RelativePointer("class_name_pointer"),
			    RelativePointer("superclass_name_pointer"),
			    ULInt32("modifiers"),
			    ULInt32("interface_count"),
			    RelativePointer("interfaces_pointer"),
			    ULInt32("rom_method_count"),
			    RelativePointer("rom_methods_pointer"),
			    ULInt32("rom_field_count"),
			    RelativePointer("rom_fields_pointer"),
			    ULInt32("object_static_count"),
			    ULInt32("double_scalar_static_count"),
			    ULInt32("ram_constant_pool_count"),
			    ULInt32("rom_constant_pool_count"),
			    ULInt32("crc"),
			    ULInt32("instance_size"),
			    ULInt32("instance_shape"),
			    RelativePointer("cp_shape_description_pointer"),
			    RelativePointer("outer_class_name_pointer"),
			    ULInt32("member_access_flags"),
			    ULInt32("inner_class_count"),
			    RelativePointer("inner_classes_pointer"),
			    ULInt16("major_version"),
			    ULInt16("minor_version"),
			    ULInt32("optional_flags"),
			    RelativePointer("optional_info_pointer"),
				Pointer(lambda ctx: ctx.class_name_pointer, PascalString("class_name", length_field=ULInt16("length"))),
				Pointer(lambda ctx: ctx.superclass_name_pointer, PascalString("superclass_name", length_field=ULInt16("length"))),
			)),
		)
	)),
)	

header = J9ROMImageHeader.parse(data)
print header

	
