PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE pelajar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        ic TEXT,
        kelas TEXT,
        asrama TEXT,
        markah INTEGER DEFAULT 100
    , jantina TEXT);
INSERT INTO pelajar VALUES(1,'dz','777','5151','1a',100,NULL);
INSERT INTO pelajar VALUES(10,'aisya','987654321','3 alfa','a1',69,'P');
INSERT INTO pelajar VALUES(11,'john taylor swifft toyota bin ahmad albab','9999','2','a5',248,'L');
INSERT INTO pelajar VALUES(12,'doremi','667676','1zeta','b15',100,'L');
INSERT INTO pelajar VALUES(13,'gshsh','hhehh','j','hh',100,'L');
INSERT INTO pelajar VALUES(17,'test','test','test','test',76,'Perempuan');
INSERT INTO pelajar VALUES(19,'MUHAMMAD RAFI BIN RAUF','111104040341','3 Omega','A6',100,'Lelaki');
CREATE TABLE rekod (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pelajar_id INTEGER,
    tarikh TEXT,
    jenis TEXT,
    keterangan TEXT,
    markah_ubah INTEGER
, markah INTEGER);
INSERT INTO rekod VALUES(1,3,'04/05/2026','KESALAHAN','berak dalam seluar',-25,-25);
INSERT INTO rekod VALUES(2,3,'04/05/2026','KESALAHAN','tidur atas jalan',-10,-10);
INSERT INTO rekod VALUES(3,4,'04/05/2026','KESALAHAN','berak merata rata',NULL,-25);
INSERT INTO rekod VALUES(4,5,'04/05/2026','KESALAHAN','kencing dalam seluar',NULL,-25);
INSERT INTO rekod VALUES(5,5,'04/05/2026','KESALAHAN','berat merata rata',NULL,-10);
INSERT INTO rekod VALUES(6,7,'04/05/2026','KESALAHAN','balik ke kubur tanpa kebenaran',NULL,-30);
INSERT INTO rekod VALUES(7,9,'2026-05-04','KESALAHAN','berak dalam seluar',NULL,-25);
INSERT INTO rekod VALUES(8,10,'2026-05-04','KESALAHAN','tido dalam peti ais',NULL,-10);
INSERT INTO rekod VALUES(9,10,'2026-05-04','KESALAHAN','belasah orang',NULL,-1);
INSERT INTO rekod VALUES(10,10,'2026-05-04','KESALAHAN','',NULL,-20);
INSERT INTO rekod VALUES(11,11,'2026-05-04','KESALAHAN','berak',NULL,-50);
INSERT INTO rekod VALUES(12,9,'2026-05-04','Kebaikan','Tolong kutip batu jalan raya',NULL,35);
INSERT INTO rekod VALUES(13,11,'2026-05-04','Kebaikan','kutip makanan atas jalan raya',NULL,99);
INSERT INTO rekod VALUES(14,11,'2026-05-04','Kebaikan','kutip makanan atas jalan raya',NULL,99);
INSERT INTO rekod VALUES(20,17,'2026-05-05','Kesalahan','mandi air longkang',NULL,-24);
PRAGMA writable_schema=ON;
CREATE TABLE IF NOT EXISTS sqlite_sequence(name,seq);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('pelajar',19);
INSERT INTO sqlite_sequence VALUES('rekod',22);
PRAGMA writable_schema=OFF;
COMMIT;
