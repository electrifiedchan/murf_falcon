import { NextResponse } from 'next/server';
import { execSync } from 'child_process';
import path from 'path';

export async function GET() {
  try {
    const backendDir = path.resolve(process.cwd(), '../backend');
    const pyScript = `import sys; sys.path.insert(0, './src'); import json, db; print(json.dumps(db.get_call_stats()))`;
    const output = execSync(`uv run python -c "${pyScript}"`, {
      cwd: backendDir,
      encoding: 'utf-8',
    });
    const stats = JSON.parse(output.trim());
    return NextResponse.json({ success: true, stats });
  } catch (error: any) {
    console.error('API /api/stats GET error:', error);
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
