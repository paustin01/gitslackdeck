""" Notifies slack from GH actions """

import argparse
import json

import requests


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--build-number", type=str, required=True)
    parser.add_argument("--build-tag", type=str, required=True)
    parser.add_argument("--repo_name", type=str)
    parser.add_argument("--rundeck-url", type=str, default="")
    parser.add_argument("--slack-channel", type=str, required=True)
    parser.add_argument("--slack-webhook", type=str, required=True)
    parser.add_argument("--committer", type=str, required=True)
    parser.add_argument("--commit-msg", type=str, default="Empty")
    parser.add_argument("--build-status", type=str, required=True)
    parser.add_argument("--team-name", type=str, required=True)
    parser.add_argument("--auto-deploys", type=str, default="false")
    args = parser.parse_args()

    auto_deploys = bool(args.auto_deploys.lower() == "true")

    # https://github.com/verana-health/remote_agent_monitor/actions/runs/1076807510
    action_url = "".join(
        [
            "https://github.com/",
            args.team_name,
            "/",
            args.repo_name,
            "/actions/runs/",
            args.build_number,
        ]
    )

    if len(args.commit_msg) > 30:
        sane_commit_msg = args.commit_msg[:30] + "..."
    else:
        sane_commit_msg = args.commit_msg

    if args.build_status == "success":
        msg_text = (
            f"*{args.committer}'s* commit in *{args.repo_name}* with message"
            f' "_{sane_commit_msg}_" built successfully'
        )

        if auto_deploys:
            msg_text += " and has already been deployed"

        actions = [
            {
                "name": "success",
                "type": "button",
                "text": f"View build (#{args.build_tag})",
                "url": action_url,
            }
        ]
        fallback_message = f"View build at {action_url}"

        if args.rundeck_url:
            actions.append(
                {
                    "name": "success",
                    "type": "button",
                    "text": "Deploy",
                    "url": args.rundeck_url,
                }
            )
            fallback_message = f"Deploy manually at {args.rundeck_url}"

        slack_msg = {
            "channel": f"#{args.slack_channel}",
            "text": msg_text,
            "attachments": [
                {"color": "#008000", "fallback": fallback_message, "actions": actions}
            ],
        }
    else:
        msg_text = (
            f"*{args.committer}'s* commit in *{args.repo_name}* with message"
            f' "_{sane_commit_msg}_" failed to build.'
        )

        slack_msg = {
            "channel": f"#{args.slack_channel}",
            "text": msg_text,
            "attachments": [
                {
                    "color": "#ff0000",
                    "fallback": f"Investigate on GitHub at {action_url}",
                    "actions": [
                        {
                            "type": "button",
                            "text": f"View build (#{args.build_tag})",
                            "style": "danger",
                            "url": action_url,
                        }
                    ],
                }
            ],
        }

    payload = json.dumps(slack_msg)
    headers = {"Content-Type": "application/json"}
    response = requests.request(
        "POST", args.slack_webhook, headers=headers, data=payload
    )
    print(response.text)


if __name__ == "__main__":
    main()
