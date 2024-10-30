import { exec } from 'child_process';
import { promisify } from 'util';
import fetch from 'node-fetch';

const execAsync = promisify(exec);

const REPO_URL = 'https://api.github.com/repos/outmaneuver/selfbot/commits';
const LOCAL_COMMIT_HASH = 'git rev-parse HEAD';

async function getLatestCommitHash() {
    const response = await fetch(REPO_URL);
    const data = await response.json();
    return data[0].sha;
}

async function getLocalCommitHash() {
    const { stdout } = await execAsync(LOCAL_COMMIT_HASH);
    return stdout.trim();
}

async function updateRepository() {
    await execAsync('git pull');
    await execAsync('bun install');
    await execAsync('bun run build');
}

export async function checkForUpdates() {
    const latestCommitHash = await getLatestCommitHash();
    const localCommitHash = await getLocalCommitHash();

    if (latestCommitHash !== localCommitHash) {
        console.log('New update available. Updating repository...');
        await updateRepository();
        console.log('Update complete. Please restart the bot.');
    } else {
        console.log('No updates available.');
    }
}
