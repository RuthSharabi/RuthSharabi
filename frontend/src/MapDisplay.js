import React, { useEffect, useState } from 'react';

const CELL_SIZE = 40;

const iconMap = {
  explosive: { emoji: '💣', color: 'red', label: 'מטען חבלה' },
  person: { emoji: '🧍', color: 'orange', label: 'דמות חשודה' },
  hostile_voice: { emoji: '🔊', color: 'yellow', label: 'שפה עוינת' },
  robot: { emoji: '🤖', color: 'blue', label: 'מיקום הרובוט' },
};

const MapDisplay = () => {
  const [mapData, setMapData] = useState({ robot_path: [], detections: [] });

  useEffect(() => {
    const fetchMapData = () => {
      fetch("http://localhost:5000/getMap")
        .then(res => res.json())
        .then(data => setMapData(data))
        .catch(err => console.error("שגיאה בקבלת נתוני מפה:", err));
    };

    fetchMapData();
    const interval = setInterval(fetchMapData, 2000);

    return () => clearInterval(interval);
  }, []);

  const renderCell = (x, y, emoji, color, title) => (
    <div
      key={`${x},${y}-${emoji}`}
      style={{
        position: 'absolute',
        left: x * CELL_SIZE,
        top: y * CELL_SIZE,
        width: CELL_SIZE,
        height: CELL_SIZE,
        backgroundColor: color,
        border: '1px solid #aaa',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '20px',
        fontWeight: 'bold',
        color: '#000',
      }}
      title={title}
    >
      {emoji}
    </div>
  );

  const robotPosition = mapData.robot_path.at(-1);

  return (
    <div style={{ display: 'flex', direction: 'rtl' }}>
      <div style={{ position: 'relative', width: 1000, height: 800, border: '3px solid black' }}>
        {/* ציור המסלול */}
        {mapData.robot_path.map(({ x, y }, i) =>
          renderCell(x, y, '', '#ccf', `שלב ${i + 1}`)
        )}

        {/* ציור הרובוט */}
        {robotPosition &&
          renderCell(robotPosition.x, robotPosition.y, iconMap.robot.emoji, iconMap.robot.color, iconMap.robot.label)}

        {/* ציור זיהויים */}
        {mapData.detections.map(({ x, y, type }, i) => {
          const icon = iconMap[type] || { emoji: '?', color: 'gray', label: 'לא ידוע' };
          return renderCell(x, y, icon.emoji, icon.color, icon.label);
        })}
      </div>

      {/* מקרא סימנים */}
      <div style={{ marginRight: 20 }}>
        <h3>🔍 מקרא סימנים</h3>
        <ul style={{ listStyleType: 'none', padding: 0, fontSize: '18px' }}>
          {Object.entries(iconMap).map(([key, { emoji, label }]) => (
            <li key={key} style={{ marginBottom: 10 }}>
              <span style={{ fontSize: '22px' }}>{emoji}</span> – {label}
            </li>
          ))}
          <li style={{ marginTop: 20, color: '#888' }}>
            ⬜ – מסלול הרובוט
          </li>
        </ul>
      </div>
    </div>
  );
};

export default MapDisplay;
