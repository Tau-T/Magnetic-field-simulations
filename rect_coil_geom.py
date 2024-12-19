import numpy as np

def rect_coil_geom(a0xi, a0yi, z0, radius):
        
    #sides of the coil
    yl = -a0yi #bottom side of inner coil
    yr = a0yi #top side of inner coil
    xr = a0xi #right side of inner coil
    xl = -a0xi #left side of inner coil

    #inner arc dimensions
    #radius = 0.0133        # Radius of the arc
    start_angle = 0      # Start angle in radians
    end_angle = np.pi/2  # End angle in radians (90 degrees)

    #inner line boundaries
    xendl = -a0xi +radius
    xendr = -xendl
    yend_b = -a0yi + radius
    yend_u = -yend_b


    ##Making the geometry of coil
    #make top half of right line
    xseg1 = np.array([xr,xr])
    yseg1 = np.array([0,yend_u])
    zseg1 = np.array([z0,z0])

    #bottom half of right line
    xseg0 = xseg1
    yseg0 = yseg1[::-1]
    zseg0 = zseg1 

    #Generate right half of top line
    x_top_right_seg = np.array([xendr,0])
    y_top_right_seg = np.array([yr,yr])
    z_top_right_seg = np.array([z0,z0])

    #Generate right half of bottom line
    x_bot_right_seg = x_top_right_seg[::-1]
    y_bot_right_seg = -y_top_right_seg[::-1]
    z_bot_right_seg = z_top_right_seg

    # Generate points along the arc

    #points for top right arc
    theta = np.linspace(start_angle, end_angle, 10)  # 100 points for smooth arc
    x = radius * np.cos(theta) + xendr # x-coordinates
    y = radius * np.sin(theta)  + yend_u # y-coordinates
    z = np.full(10,z0)        # z-coordinates (arc in the xy-plane)

    #append the radius to line segment

    xseg1 = np.append(xseg1, x)
    yseg1 = np.append(yseg1, y)
    zseg1 = np.append(zseg1, z)

    yseg0 = -yseg1[::-1]
    xseg0 = xseg1[::-1]
    zseg0 = zseg1[::-1]

    #Add the left half of the coil
    xtotal = np.append(xseg0,xseg1)
    ytotal = np.append(yseg0,yseg1)
    ztotal = np.append(zseg0, zseg1)

    xtotal = np.concatenate((x_bot_right_seg, xtotal, x_top_right_seg),0)
    ytotal = np.concatenate((y_bot_right_seg, ytotal, y_top_right_seg),0)
    ztotal = np.concatenate((z_bot_right_seg, ztotal, z_top_right_seg),0)

    xtotal = np.concatenate((-xtotal[::-1], xtotal),0)
    ytotal = np.concatenate((ytotal[::-1], ytotal ),0)
    ztotal = np.concatenate((ztotal, ztotal),0)

    return(xtotal, ytotal, ztotal )