import v1.report._


def setup(app, prefix):
    prefix = prefix + '/report'

    v1.report._.setup(app, prefix)
