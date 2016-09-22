project (UQTk)

SET(copy_FILES
 uq_pc.py
 model.py
 plot.py
 plot_prep.py
 model_sens.x
 pdomain_3d.txt
 )


INSTALL(FILES ${copy_FILES} 
        PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ 
        DESTINATION examples/uqpc)
