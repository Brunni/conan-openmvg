from conans import ConanFile, CMake, tools
import os

class OpenMvgConan(ConanFile):
	name = "openmvg"
	version = "1.1"
	license = "Unlicense"
	url = "https://github.com/Brunni/conan-openmvg"
	description = "open Multiple View Geometry is a library for computer-vision scientists and especially targeted to the Multiple View Geometry community."
	settings = "os", "compiler", "build_type", "arch"
	options = {"shared": [True, False]}
	default_options = "shared=False"
	generators = "cmake"
	short_paths=True
	
	def config(self):
#		if self.scope.dev and self.scope.build_tests:
#			self.requires( "gtest/1.8.0@lasote/stable" )
#			self.options["gtest"].shared = False
		print("Description is: %s" % self.description)
		print("default_option is: %s" % self.default_options)
		print("shared is: %s" % self.options.shared)

	def requirements(self):
		print("requires need to be defined correctly")
		#self.requires("cereal/1.2-0@TimSimpson/testing")
		#self.requires("cereal/1.2.2@Brunni/stable")
		#self.requires("GLFW/3.2.1@Brunni/prebuilt")
		#self.requires("osi_clp/master@Brunni/testing")
#		 self.requires("giflib/5.1.3@lasote/stable")
#		self.requires("libpng/1.6.21@lasote/stable")
#		 self.requires("libjpeg-turbo/1.4.2@lasote/stable")

	def source(self):
		self.run("git clone --depth 1 --recursive https://github.com/openMVG/openMVG.git -b v%s" % self.version)
		# step 1 would be to dismiss the --recursive stuff
		#self.run("cd openMVG && git submodule update --init --recursive")
		#self.run("cd hello && git checkout static_shared")
		# This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
		# if the packaged project doesn't have variables to set it properly
		tools.replace_in_file("openMVG/src/CMakeLists.txt", "project(openMVG C CXX)", '''project(openMVG C CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')
		#tools.replace_in_file("openMVG/src/CMakeLists.txt", "NOT EXISTS ${PROJECT_SOURCE_DIR}/dependencies/cereal/include", "EXISTS #${PROJECT_SOURCE_DIR}/dependencies/cereal/include")

	def build(self):
		cmake = CMake(self.settings)
		cmake_opts = "-DUSE_CONAN=True "
		cmake_opts += "-DOpenMVG_BUILD_TESTS=ON " if self.scope.dev and self.scope.build_tests else "-DOpenMVG_BUILD_TESTS=OFF "
		if self.options.shared:
			print("Building shared lib only")
			cmake_opts += "-DOpenMVG_BUILD_SHARED=ON "
		else:
			print("Building static lib only")
			cmake_opts += "-DOpenMVG_BUILD_SHARED=OFF "
		
		cmake_opts += "-DOpenMVG_BUILD_EXAMPLES=OFF "
		cmake_opts += "-DOpenMVG_BUILD_DOC=OFF "
		cmake_opts += "-DSCHUR_SPECIALIZATIONS=OFF "
		self.run('cmake %s/openMVG/src %s %s' % (self.conanfile_directory, cmake.command_line, cmake_opts))
		# We need to prevent to build static library as well when building shared. It might overwrite the lib file!
		self.run("cmake --build . %s " % cmake.build_config)

	def package(self):
		self.copy("*.hpp", dst="include/openMVG", src="openMVG/src/openMVG")
		self.copy("*.h", dst="include/openMVG", src="openMVG/src/openMVG")
		self.copy("*.hpp", dst="include", src="openMVG/src/dependencies/cereal/include") #ceres
		self.copy("*.h", dst="include", src="openMVG/src/dependencies/cereal/include") #ceres
		self.copy("*.hpp", dst="include", src="openMVG/src/dependencies/osi_clp/CoinUtils/src") #ceres
		self.copy("*.h", dst="include", src="openMVG/src/dependencies/osi_clp/CoinUtils/src") #ceres
		self.copy("*.hpp", dst="include/third_party/stlplus3", src="openMVG/src/third_party/stlplus3/") #third party stlplus3
		self.copy("*.h", dst="include/third_party/stlplus3", src="openMVG/src/third_party/stlplus3") #third party stlplus3
		self.copy("*.hpp", dst="include/lemon", src="openMVG/src/third_party/lemon/lemon") #third party lemon
		self.copy("*.h", dst="include/lemon", src="openMVG/src/third_party/lemon/lemon") #third party lemon
		self.copy("*.hpp", dst="include", src="openMVG/src/third_party/ceres-solver/include") #third party ceres
		self.copy("*.h", dst="include", src="openMVG/src/third_party/ceres-solver/include") #third party ceres
		self.copy("*.lib", dst="lib", keep_path=False)
		self.copy("*.exp", dst="lib", src="Release", keep_path=False)
		self.copy("*.dll", dst="bin", src="Release", keep_path=False) #shared lib
		self.copy("*.so", dst="lib", src="", keep_path=False)
		self.copy("*.a", dst="lib", src="", keep_path=False)

	def package_info(self):
		self.cpp_info.libs = [
			"ceres",
			"cxsparse",
			"easyexif",
			"fast",
			"jpeg", # Should be used from conan package like many other libs here.
			"lemon",
			"lib_clp",
			"lib_CoinUtils",
			"lib_Osi",
			"lib_OsiClpSolver",
			"openMVG_features",
			"openMVG_image",
			"openMVG_kvld",
			"openMVG_lInftyComputerVision",
			"openMVG_main_ColHarmonize",
			"openMVG_main_ComputeFeatures",
			"openMVG_main_ComputeMatches",
			"openMVG_main_ComputeSfM_DataColor",
			"openMVG_main_ComputeStructureFromKnownPoses",
			"openMVG_main_ConvertList",
			"openMVG_main_ConvertSfM_DataFormat",
			"openMVG_main_evalQuality",
			"openMVG_main_ExportCameraFrustums",
			"openMVG_main_exportKeypoints",
			"openMVG_main_exportMatches",
			"openMVG_main_exportTracks",
			"openMVG_main_ExportUndistortedImages",
			"openMVG_main_FrustumFiltering",
			"openMVG_main_geodesy_registration_to_gps_position",
			"openMVG_main_GlobalSfM",
			"openMVG_main_IncrementalSfM",
			"openMVG_main_ListMatchingPairs",
			"openMVG_main_openMVG2CMPMVS",
			"openMVG_main_openMVG2MESHLAB",
			"openMVG_main_openMVG2MVE2",
			"openMVG_main_openMVG2MVSTEXTURING",
			"openMVG_main_openMVG2NVM",
			"openMVG_main_openMVG2openMVS",
			"openMVG_main_openMVG2PMVS",
			"openMVG_main_SfMInit_ImageListing",
			"openMVG_main_SfM_Localization",
			"openMVG_matching",
			"openMVG_matching_image_collection",
			"openMVG_multiview",
			"openMVG_multiview_test_data",
			"openMVG_numeric",
			"openMVG_sfm",
			"openMVG_system",
			"png",
			"stlplus",
			"tiff",
			"vlsift",
			"zlib"]
		
