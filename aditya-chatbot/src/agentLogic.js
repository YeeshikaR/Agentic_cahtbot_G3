const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1)

export const AGENTS = [
  { id: 'venue', name: 'Agent Venue Manager' },
  { id: 'coordinator', name: 'Agent Coordinator' },
  { id: 'designer', name: 'Agent Designer' },
  { id: 'logistics', name: 'Agent Logistics' },
  { id: 'finance', name: 'Agent Finance' },
  { id: 'outreach', name: 'Agent Outreach' },
]

const KEYWORD_TEMPLATES = [
  {
    pattern: /(workshop|seminar|webinar)/i,
    subtasks: [
      'Define objectives & audience',
      'Book venue / setup meeting link',
      'Invite coordinator & speakers',
      'Design promotional poster',
      'Publish registration form',
      'Arrange logistics & equipment',
      'Send reminders & finalize schedule'
    ],
  },
  {
    pattern: /(competition|hackathon|contest)/i,
    subtasks: [
      'Finalize theme & rules',
      'Confirm judges & mentors',
      'Create timeline & rounds',
      'Design poster & website section',
      'Sponsor outreach & budget plan',
      'Volunteer allocation & venues'
    ],
  },
  {
    pattern: /(meeting|review|standup)/i,
    subtasks: [
      'Set agenda & goals',
      'Pick time & room/online link',
      'Send calendar invites',
      'Prepare minutes template',
      'Record action items'
    ],
  },
  {
    pattern: /(trip|visit|industrial visit|tour)/i,
    subtasks: [
      'Decide destination & dates',
      'Budgeting & approvals',
      'Transport & accommodation',
      'Permissions & safety brief',
      'Itinerary & contacts list'
    ],
  },
  {
    pattern: /(website|portal|bot|chatbot|app)/i,
    subtasks: [
      'Clarify requirements & scope',
      'Create task breakdown & UI wireframes',
      'Setup repo & CI/CD',
      'Implement MVP features',
      'QA, bugfix & deploy'
    ],
  }
]

function genericPlan(query) {
  const topic = query.trim().replace(/\.$/, '')
  return [
    `Understand goal: ${cap(topic)}`,
    'Create task list & timeline',
    'Assign owners & resources',
    'Prepare communication & assets',
    'Execute & track progress',
    'Review outcomes & next steps',
  ]
}

export function deriveSubtasks(query) {
  for (const t of KEYWORD_TEMPLATES) {
    if (t.pattern.test(query)) return t.subtasks
  }
  return genericPlan(query)
}

export function assignAgentsToSubtasks(subtasks) {
  return subtasks.map((task, i) => ({
    id: `${i}`,
    task,
    agent: AGENTS[i % AGENTS.length].name,
    status: 'pending',
    logs: [],
  }))
}

export function simulate(subtaskItems, { onTick, speed = 1 }) {
  const timers = []
  let base = 400
  const factor = 1 / speed

  subtaskItems.forEach((item, idx) => {
    const startDelay = Math.round((base + idx * 300) * factor)
    const workDelay = Math.round((600 + Math.random() * 700) * factor)

    timers.push(
      setTimeout(() => {
        item.status = 'in_progress'
        item.logs.push(`${item.agent}: Starting → ${item.task}`)
        onTick(item, idx)

        timers.push(
          setTimeout(() => {
            item.status = 'done'
            item.logs.push(`${item.agent}: Completed ✓`)
            onTick(item, idx)
          }, workDelay)
        )
      }, startDelay)
    )
  })

  return {
    cancel: () => timers.forEach(clearTimeout)
  }
}
