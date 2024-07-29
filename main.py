from string import Template

from pyaction import PyAction
from pyaction.auth import Auth
from pyaction.issues import IssueForm
from sighted import Literal
from sighted.language import PoS

workflow = PyAction()

COLORS = {
    "Gray": "{gray}",
    "Light Gray": "{lightgray}",
    "Dark Gray": "{lightgray}",
    "Red": "{red}",
    "Yellow": "{yellow}",
    "Green": "{green}",
}


@workflow.action()
def my_action(github_token: str, repository: str, issue_number: int) -> None:
    auth = Auth(token=github_token)

    repo = auth.github.get_repo(repository)
    user_input = IssueForm(repo=repo, number=issue_number).render()

    language = Literal(
        text=user_input["Text"],
        fixation=int(user_input["Fixation"]),
        saccade=int(user_input["Saccade"]),
        ignore_pos=[PoS.PUNCT],
    )

    color = COLORS[user_input["Color"]]
    prefix, postfix = f"$`\color{color}", "`$"

    transformed_text = language.transform(
        template=Template(f" $`$fix`$${prefix}$unfix{postfix}")
    )

    workflow.write({"bionic_text": "".join(list(transformed_text))})
