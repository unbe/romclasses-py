import sys

from construct import *

input = open(sys.argv[1], "rb")
data = input.read()
input.close()

def deco(obj, ctx):
	if obj._ptr == 0:
		print "Obj: " + repr(obj)
		print "Ctx: " + repr(ctx)
	return obj._base + obj._ptr

def Relative(name):
	return ExprAdapter(Struct(name, Anchor("base"), SLInt32("ptr")), 
		encoder = None,
		decoder = lambda obj, ctx: obj.base + obj.ptr if obj.ptr != 0 else None)
		#decoder = deco)

def Carp(ptr, ctx, struct):
	addr = ptr(ctx)
	if addr is None:
		print "None: " + repr(ctx)
		print struct
		return 0
	return addr
		

def MaybePointer(ptr, struct):
	return If(lambda ctx: ptr(ctx) is not None, Pointer(ptr, struct))

def StringPointer(ptr, name):
	return MaybePointer(ptr, PascalString(name, length_field=ULInt16("length")))

def StringRef(name):
	return ExprAdapter(
		Struct(name, 
			Relative("ptr"), 
			StringPointer(lambda ctx: ctx.ptr, "str")
		),
		encoder = None,
		decoder = lambda obj, ctx: obj.str)
	

J9ROMImageHeader = Struct("J9ROMImageHeader",
	Enum(ULInt32("signature"),
		CORRECT = 1245264202,
		_default_ = Pass,
	),
	ULInt32("flags_and_version"),
	ULInt32("rom_size"),
	ULInt32("class_count"),
	Relative("jxe_pointer"),
	Relative("toc_pointer"),
	Relative("first_class_pointer"),
	Relative("aot_pointer"),
	Array(16, ULInt8("symbol_file_id")),
	Pointer(lambda ctx: ctx.toc_pointer, Array(lambda ctx: ctx.class_count, 
		Struct("J9ROMClassTOCEntry",
			StringRef("class_name"),
			Relative("class_pointer"),
			MaybePointer(lambda ctx: ctx.class_pointer, Struct("J9ROMClass",
			    ULInt32("rom_size"),
			    ULInt32("single_scalar_static_count"),
			    StringRef("class_name"),
			    StringRef("superclass_name"),
			    ULInt32("modifiers"),
			    ULInt32("interface_count"),
			    Relative("interfaces_pointer"),
			    ULInt32("rom_method_count"),
			    Relative("rom_methods_pointer"),
			    ULInt32("rom_field_count"),
			    Relative("rom_fields_pointer"),
			    ULInt32("object_static_count"),
			    ULInt32("double_scalar_static_count"),
			    ULInt32("ram_constant_pool_count"),
			    ULInt32("rom_constant_pool_count"),
			    ULInt32("crc"),
			    ULInt32("instance_size"),
			    ULInt32("instance_shape"),
			    Relative("cp_shape_description_pointer"),
			    StringRef("outer_class_name_pointer"),
			    ULInt32("member_access_flags"),
			    ULInt32("inner_class_count"),
			    Relative("inner_classes_pointer"),
			    ULInt16("major_version"),
			    ULInt16("minor_version"),
			    ULInt32("optional_flags"),
			    Relative("optional_info_pointer"),
					MaybePointer(lambda ctx: ctx.interfaces_pointer, Array(lambda ctx: ctx.interface_count, StringRef("interfaces"))),
					If(lambda ctx: ctx.class_name == 'java/util/MapEntry', MaybePointer(lambda ctx: ctx.rom_methods_pointer, Array(lambda ctx: min(4, ctx.rom_method_count), Struct("method",
						Relative("name"),
						Relative("signature"),
						ULInt32("modifiers"),
						ULInt16("max_stack"),
						ULInt24("bytecode_size"),
						ULInt8("arg_count"),
						ULInt16("temp_count"),
					)))),
			)),
		)
	)),
)	

header = J9ROMImageHeader.parse(data)
print header

	
