svn status | grep '^?' | awk '{print $2}' | xargs svn add
svn status | grep '^!' | awk '{print $2}' | xargs svn delete
svn commit -m "Processed unversioned and missing files"