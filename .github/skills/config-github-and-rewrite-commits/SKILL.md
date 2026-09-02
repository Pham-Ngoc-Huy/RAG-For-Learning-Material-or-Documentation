---
name: config-github-and-rewrite-commits
description: Use ONLY when GitHub is not counting contributions because commits show the wrong author (e.g. macOS full name "Phạm Huy" / email whoami@Phams-MacBook-Air.local instead of the GitHub username and verified email), when git config user.name/user.email is missing or wrong, or when rewriting existing commit authors on past commits via filter-branch.
---

# Fix GitHub commit attribution (config + rewrite history)

Vấn đề: GitHub count contribution theo **email** của author trong commit, KHÔNG theo
SSH key. SSH chỉ xác thực push. Nếu `user.email` khác email GitHub đã verify hoặc
không match, commit không được tính.

Dấu hiệu: commit hiện author name là tên full macOS (vd `Phạm Huy`) và email dạng
`whoami@...local`.

## Bước 1 — Chẩn đoán

```bash
git config --global user.name
git config --global user.email
git config --local user.name
git config --local user.email
git log --format="%h | %an <%ae> | %cn <%ce>" -5
git var GIT_AUTHOR_IDENT
```

Nếu `GIT_AUTHOR_IDENT` trả ra name/email không phải danh tính GitHub → config
thiếu hoặc sai.

## Bước 2 — Set config đúng

```bash
git config --global user.name "<github-username>"
git config --global user.email "<github-verified-email>"
git var GIT_AUTHOR_IDENT   # verify
```

Danh tính phải khớp email GitHub đã verify trong Settings → Emails.

## Bước 3 — Kiểm tra toàn cảnh trước khi rewrite

```bash
git log --format="%h | %an <%ae> | %s" main -20
git rev-list --left-right --count origin/main...main   # detect divergence
git diff --stat main origin/main                       # content có giống nhau không
git branch -r
```

Cảnh báo: nếu local và origin diverge, force push sẽ ghi đè — phải xác nhận
content bằng nhau trước khi làm.

## Bước 4 — Backup + rewrite lịch sử bằng filter-branch

```bash
git branch backup-main-before-author-fix
```

Rewrite mọi commit mang email sai (đổi cả AUTHOR lẫn COMMITTER):

```bash
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --env-filter '
if [ "$GIT_AUTHOR_EMAIL" = "<email-sai>" ]; then
    GIT_AUTHOR_NAME="<github-username>"
    GIT_AUTHOR_EMAIL="<github-verified-email>"
fi
if [ "$GIT_COMMITTER_EMAIL" = "<email-sai>" ]; then
    GIT_COMMITTER_NAME="<github-username>"
    GIT_COMMITTER_EMAIL="<github-verified-email>"
fi
' -- main
```

Lưu ý điều kiện dùng `=` (so sánh chuỗi) và `GIT_AUTHOR_EMAIL` (không phải
`GIT_AUTHOR_NAME`) để không ghi đè nhầm commit của người khác.

## Bước 5 — Verify local

```bash
git log main --format="%h %an <%ae>" -8
git log main --format="%ae" | grep -c "<email-sai>" || echo "0 (sạch)"
```

## Bước 6 — Force push

```bash
git push --force-with-lease origin main
git log origin/main --format="%h %an <%ae>" -6   # verify remote
```

## Sau khi xong

1. Khiến người dùng thêm email của họ vào GitHub **Settings → Settings → Emails**
   (nếu chưa có) để contributions hiển thị đầy đủ.
2. Commit RE-write sẽ đổi hash → history bị broken cho ai clone cũ; global config
   mới đảm bảo các commit tương lai đúng author.
3. Giữ branch backup (`backup-main-before-author-fix`) đến khi chắc chắn, rồi
   xóa: `git branch -D backup-main-before-author-fix` (và `git update-ref -d refs/original/...` nếu cần).
