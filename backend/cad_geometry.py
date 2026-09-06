"""
Parametric 3D CAD Wireframe & Surface Generator
Generates Plotly 3D CAD visualizers for thermal shelter geometry, openings, and azimuth orientation.
"""
import numpy as np
import plotly.graph_objects as go

def generate_shelter_3d_cad_figure(length, width, height, shape="Rectangular", window_area=1.5, door_area=2.0, orientation_deg=0.0):
    """
    Creates interactive 3D CAD Plotly figure of shelter geometry, roof shape, openings, and orientation.
    """
    l, w, h = float(length), float(width), float(height)
    
    # 8 Corner vertices of box
    v = np.array([
        [0, 0, 0], [l, 0, 0], [l, w, 0], [0, w, 0], # Floor 0..3
        [0, 0, h], [l, 0, h], [l, w, h], [0, w, h]  # Eave 4..7
    ])

    # Roof peak vertices if Gable or Monoslope
    if shape == "Gable":
        r_peak_h = h + 0.8
        v_g1 = np.array([0, w/2, r_peak_h])
        v_g2 = np.array([l, w/2, r_peak_h])
    elif shape == "Monoslope":
        r_peak_h = h + 0.8
        v[4][2] = r_peak_h
        v[5][2] = r_peak_h

    fig = go.Figure()

    # Draw Wall Bounding Wireframe Edges
    edges = [
        (0,1), (1,2), (2,3), (3,0), # Floor ring
        (4,5), (5,6), (6,7), (7,4), # Eave ring
        (0,4), (1,5), (2,6), (3,7)  # Vertical corners
    ]

    for edge in edges:
        p1, p2 = v[edge[0]], v[edge[1]]
        fig.add_trace(go.Scatter3d(
            x=[p1[0], p2[0]], y=[p1[1], p2[1]], z=[p1[2], p2[2]],
            mode='lines',
            line=dict(color='#00F0FF', width=4),
            showlegend=False
        ))

    # Add Gable roof ridge lines
    if shape == "Gable":
        fig.add_trace(go.Scatter3d(
            x=[v_g1[0], v_g2[0]], y=[v_g1[1], v_g2[1]], z=[v_g1[2], v_g2[2]],
            mode='lines',
            line=dict(color='#FF8F00', width=5),
            name='Roof Ridge Peak'
        ))
        # Rafters
        for e in [(4, v_g1), (7, v_g1), (5, v_g2), (6, v_g2)]:
            p1 = v[e[0]]
            p2 = e[1]
            fig.add_trace(go.Scatter3d(
                x=[p1[0], p2[0]], y=[p1[1], p2[1]], z=[p1[2], p2[2]],
                mode='lines',
                line=dict(color='#FF8F00', width=3),
                showlegend=False
            ))

    # Draw Window Glazing Opening on South Wall (y=0 plane -> surfaceaxis=1)
    if window_area > 0:
        win_w = min(l * 0.4, np.sqrt(window_area * 1.5))
        win_h = min(h * 0.5, window_area / win_w)
        win_x0 = (l - win_w) / 2
        win_z0 = (h - win_h) / 2
        
        wx = [win_x0, win_x0 + win_w, win_x0 + win_w, win_x0, win_x0]
        wy = [0, 0, 0, 0, 0]
        wz = [win_z0, win_z0, win_z0 + win_h, win_z0 + win_h, win_z0]

        fig.add_trace(go.Scatter3d(
            x=wx, y=wy, z=wz,
            mode='lines+markers',
            surfaceaxis=1, # Fill surface along y-plane
            surfacecolor='rgba(0, 240, 255, 0.4)',
            line=dict(color='#00F0FF', width=3),
            name=f'Window ({window_area:.1f} m²)'
        ))

    # Draw Door Opening on West Wall (x=0 plane -> surfaceaxis=0)
    if door_area > 0:
        door_w = 0.9
        door_h = min(h * 0.85, door_area / door_w)
        door_y0 = (w - door_w) / 2
        
        dx = [0, 0, 0, 0, 0]
        dy = [door_y0, door_y0 + door_w, door_y0 + door_w, door_y0, door_y0]
        dz = [0, 0, door_h, door_h, 0]

        fig.add_trace(go.Scatter3d(
            x=dx, y=dy, z=dz,
            mode='lines+markers',
            surfaceaxis=0, # Fill surface along x-plane
            surfacecolor='rgba(239, 68, 68, 0.4)',
            line=dict(color='#EF4444', width=3),
            name=f'Door ({door_area:.1f} m²)'
        ))

    # Draw Orientation Azimuth Compass Vector Arrow
    rad = np.radians(orientation_deg)
    arrow_len = max(l, w) * 0.6
    ax = l/2 + arrow_len * np.sin(rad)
    ay = w/2 - arrow_len * np.cos(rad)

    fig.add_trace(go.Scatter3d(
        x=[l/2, ax], y=[w/2, ay], z=[0, 0],
        mode='lines+markers',
        marker=dict(size=[0, 6], color='#10B981'),
        line=dict(color='#10B981', width=6),
        name=f'South Sun Vector ({orientation_deg}°)'
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title='Length (m)', backgroundcolor="rgba(15,23,42,0.6)", gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(title='Width (m)', backgroundcolor="rgba(15,23,42,0.6)", gridcolor="rgba(255,255,255,0.1)"),
            zaxis=dict(title='Height (m)', backgroundcolor="rgba(15,23,42,0.6)", gridcolor="rgba(255,255,255,0.1)"),
            aspectmode='data',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        ),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0", family="Plus Jakarta Sans, sans-serif"),
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(15,23,42,0.8)", font=dict(color="#F1F5F9"))
    )
    return fig

if __name__ == "__main__":
    fig = generate_shelter_3d_cad_figure(6.0, 4.0, 2.4, "Gable", 1.8, 2.0, 0)
    print("3D CAD Generator successfully tested!")
