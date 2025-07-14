#!/bin/csh
# Sample OceanOnlyComp.csh . intel18 repro

set version="REPRO"
set fms_version="FMS2"
set platform="ncrc6.intel23"
set rootdir = `dirname $0`
source ${rootdir}/envs.${platform}

mkdir -p build/${platform}/fms/$version
(cd build/${platform}/fms/$version/; rm -f path_names; \
../../../../src/mkmf/bin/list_paths -l ../../../../src/FMS; \
../../../../src/mkmf/bin/mkmf -t ../../../../src/mkmf/templates/ncrc5-intel.mk -p libfms.a -c "-Duse_libMPI -Duse_netCDF -DHAVE_GETTID" path_names)
(cd build/${platform}/fms/$version/; make NETCDF=3 $version=1 libfms.a -j)


mkdir -p build/${platform}/ocean_only/${version}/
(cd build/${platform}/ocean_only/${version}/; rm -f path_names; \
../../../../src/mkmf/bin/list_paths -l ./ \
                                       ../../../../src/MOM6/config_src/infra/${fms_version} \
                                       ../../../../src/MOM6/config_src/memory/dynamic_symmetric \
                                       ../../../../src/MOM6/config_src/drivers/solo_driver \
                                       ../../../../src/MOM6/config_src/external \
                                       ../../../../src/MOM6/src/*/ \
                                       ../../../../src/MOM6/src/*/*/ \
)
(cd build/${platform}/ocean_only/${version}/; \
../../../../src/mkmf/bin/mkmf -t ../../../../src/mkmf/templates/ncrc5-intel.mk -o "-I../../fms/REPRO" -p MOM6 -l "-L../../fms/REPRO -lfms" -c '-DUSE_FMS2_IO' path_names )
(cd build/${platform}/ocean_only/${version}/; make NETCDF=3 $version=1 MOM6 -j)
