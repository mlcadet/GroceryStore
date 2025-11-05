"""Run DB migration safely:
1. Attempt to run mysqldump to create a backup (if mysqldump is available)
2. Connect using mysql.connector and execute the SQL statements from migrations/upgrade_001.sql

Usage:
  python backend/run_migration.py

This script requires the same credentials as in `sql_connection.py` (root/Steelbed@386).
It will stop on error and print the failing statement.
"""
import subprocess
import shutil
import os
import sys
import mysql.connector
from mysql.connector import Error

ROOT = os.path.dirname(os.path.abspath(__file__))
MIGRATION_SQL = os.path.join(ROOT, 'migrations', 'upgrade_001.sql')
BACKUP_PATH = os.path.join(ROOT, 'gs_backup.sql')

# Credentials (keep in sync with sql_connection.py)
DB_CONFIG = {
    'user': 'root',
    'password': 'Steelbed@386',
    'host': '127.0.0.1',
    'database': 'gs'
}


def run_mysqldump(backup_file):
    # Look for mysqldump in PATH first
    mysqldump = shutil.which('mysqldump')
    if not mysqldump:
        # Try common MySQL installation path on Windows
        possibles = [
            r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe",
            r"C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysqldump.exe"
        ]
        for p in possibles:
            if os.path.exists(p):
                mysqldump = p
                break

    if not mysqldump:
        print("mysqldump not found on PATH. Skipping automatic backup.")
        print(f"Please run: mysqldump -u {DB_CONFIG['user']} -p {DB_CONFIG['database']} > {backup_file}")
        return False

    cmd = [mysqldump, '-u', DB_CONFIG['user'], f"-p{DB_CONFIG['password']}", DB_CONFIG['database']]
    print('Running:', ' '.join(cmd))
    try:
        with open(backup_file, 'wb') as f:
            proc = subprocess.Popen(cmd, stdout=f, stderr=subprocess.PIPE)
            _, err = proc.communicate()
            if proc.returncode != 0:
                print('mysqldump failed:', err.decode())
                return False
        print('Backup saved to', backup_file)
        return True
    except Exception as e:
        print('Failed to run mysqldump:', e)
        return False


def apply_sql_file(sql_file):
    print('Applying migration:', sql_file)
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql = f.read()
        # mysql.connector C extension cursor may not support multi=True in some builds.
        # Safely split statements on ';' and execute them one by one. This is
        # sufficient for our simple migration SQL file. For more complex SQL
        # (with procedures, triggers or ; inside strings) consider using a
        # proper SQL parser or running the file via the mysql client.
        statements = [s.strip() for s in sql.split(';') if s.strip()]
        for stmt in statements:
            try:
                cursor.execute(stmt)
            except Error as e:
                print('Failed executing statement:\n', stmt)
                raise
        conn.commit()
        cursor.close()
        conn.close()
        print('Migration applied successfully.')
        return True
    except Error as e:
        print('Error applying migration:', e)
        try:
            if conn and conn.is_connected():
                conn.rollback()
                conn.close()
        except Exception:
            pass
        return False


def main():
    if not os.path.exists(MIGRATION_SQL):
        print('Migration SQL not found:', MIGRATION_SQL)
        sys.exit(1)

    print('Attempting to create backup before applying migration...')
    ran_backup = run_mysqldump(BACKUP_PATH)
    if not ran_backup:
        ans = input('Backup was not created automatically. Continue anyway? (y/N): ')
        if ans.strip().lower() != 'y':
            print('Aborting migration.')
            sys.exit(1)

    ok = apply_sql_file(MIGRATION_SQL)
    if not ok:
        print('Migration failed. Please inspect the SQL and the DB state. Backup (if created) is at', BACKUP_PATH)
        sys.exit(1)


if __name__ == '__main__':
    main()
