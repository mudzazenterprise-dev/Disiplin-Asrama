CREATE TABLE pelajar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        ic TEXT,
        kelas TEXT,
        asrama TEXT,
        markah INTEGER DEFAULT 100
    , jantina TEXT);
INSERT INTO pelajar VALUES(1,'dz','777','5151','1a',100,NULL),
  (10,'aisya','987654321','3 alfa','a1',69,'P'),
  (11,'john taylor swifft toyota bin ahmad albab','9999','2','a5',248,'L'),
  (12,'doremi','667676','1zeta','b15',100,'L'),
  (13,'gshsh','hhehh','j','hh',100,'L'),
  (17,'test','test','test','test',76,'Perempuan'),
  (19,'MUHAMMAD RAFI BIN RAUF','111104040341','3 Omega','A6',100,'Lelaki');
