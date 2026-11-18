// A practice run selects complete source question groups in printed order.
export function selectSourceGroups(index, selected) {
  const wanted = new Set(selected);
  return index.groups.filter(group => wanted.has(group.label));
}

export function sourceGroupPages(document, group) {
  return document.pageImages.slice(group.firstPage - 1, group.lastPage);
}
