class SurveyError(Exception):
    pass


class IncorrectOrgNodeValueError(SurveyError):
    pass


class ColumnMissingCodeValueError(SurveyError):
    pass


class ColumnMissingTextValueError(SurveyError):
    pass


class ColumnMinValueMustBeSmallerThanMaxValueError(SurveyError):
    pass
