const form = document.getElementById("create-form");
const message = document.getElementById("message");
const linksRoot = document.getElementById("links");
const filterSelect = document.getElementById("status-filter");

async function loadLinks() {
  const response = await fetch(`/api/links?status=${encodeURIComponent(filterSelect.value)}`);
  const payload = await response.json();
  renderLinks(payload.items || []);
}

function renderLinks(items) {
  if (!items.length) {
    linksRoot.innerHTML = "<p>No links yet.</p>";
    return;
  }

  linksRoot.innerHTML = items
    .map((item) => {
      const shortUrl = `${window.location.origin}/r/${item.code}`;
      const expiry = item.expires_at ? new Date(item.expires_at).toLocaleString() : "Never";
      return `
        <article class="card">
          <strong>${item.code}</strong>
          <p><a href="${shortUrl}" target="_blank" rel="noreferrer">${shortUrl}</a></p>
          <p class="meta">Target: ${item.target_url}</p>
          <p class="meta">Clicks: ${item.clicks} | Expired: ${item.expired ? "Yes" : "No"} | Expires: ${expiry}</p>
          <div class="actions">
            <button class="ghost" data-copy="${shortUrl}">Copy</button>
            <button class="danger" data-delete="${item.code}">Delete</button>
          </div>
        </article>
      `;
    })
    .join("");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  message.textContent = "";

  const targetUrl = document.getElementById("target-url").value.trim();
  const expiresField = document.getElementById("expires-at").value;
  const payload = {
    target_url: targetUrl,
    expires_at: expiresField ? new Date(expiresField).toISOString() : "",
  };

  const response = await fetch("/api/links", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const body = await response.json();
  if (!response.ok) {
    message.textContent = body.error || "Could not create link.";
    return;
  }

  message.textContent = `Created short code ${body.code}`;
  form.reset();
  await loadLinks();
});

filterSelect.addEventListener("change", loadLinks);

linksRoot.addEventListener("click", async (event) => {
  const copyTarget = event.target.dataset.copy;
  const deleteTarget = event.target.dataset.delete;

  if (copyTarget) {
    await navigator.clipboard.writeText(copyTarget);
    message.textContent = "Short link copied to clipboard.";
    return;
  }

  if (deleteTarget) {
    const response = await fetch(`/api/links/${deleteTarget}`, { method: "DELETE" });
    const body = await response.json();
    message.textContent = response.ok ? `Deleted ${body.deleted}` : body.error;
    await loadLinks();
  }
});

loadLinks();
