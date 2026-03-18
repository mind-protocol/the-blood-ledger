/**
 * GET /api/scenarios - List all available scenarios
 *
 * Reads scenario YAML files from the scenarios/ directory.
 * Returns metadata for scenario selection screen.
 */

import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'
import yaml from 'js-yaml'

interface ScenarioMeta {
  id: string
  name: string
  location: string
  tagline: string
  tone: string
  starts_with: string[]
}

export async function GET() {
  const scenariosDir = path.join(process.cwd(), '..', 'scenarios')

  try {
    const files = fs.readdirSync(scenariosDir)
      .filter(f => f.endsWith('.yaml'))

    const scenarios: ScenarioMeta[] = []

    for (const file of files) {
      const content = fs.readFileSync(path.join(scenariosDir, file), 'utf-8')
      const data = yaml.load(content) as any

      scenarios.push({
        id: data.id,
        name: data.name,
        location: data.location,
        tagline: data.tagline,
        tone: data.tone,
        starts_with: data.starts_with || []
      })
    }

    return NextResponse.json({ scenarios })
  } catch (error) {
    console.error('Failed to load scenarios:', error)
    return NextResponse.json(
      { error: 'Failed to load scenarios' },
      { status: 500 }
    )
  }
}
